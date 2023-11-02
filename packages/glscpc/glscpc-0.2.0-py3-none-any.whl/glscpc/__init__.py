import enum
import glob
import json
import logging
import os
import subprocess
from typing import Any, BinaryIO, Iterator

import click
import ruamel.yaml
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from ruamel.yaml.scalarstring import LiteralScalarString

"""
Documentation used to create this file: https://docs.gitlab.com/ee/ci/yaml/index.html

Important things of note:
- before_script and script are concatenated in reality, but we don't do that to keep track of line numbers.
- Unused (template) scripts are also checked.
"""

LOG = logging.getLogger("glscpc")

INCLUDE = "include"
LOCAL = "local"

GLOBAL_KEYWORDS = {
    # Default is missing because it also has script keys, we want to treat it like a job.
    INCLUDE,
    "stages",
    "variables",
    "workflow",
    "image",
    "services",
    "cache",
    "before_script",  # Deprecated
    "after_script",  # Deprecated
}

COLORS = {
    "error": "red",
    "warning": "yellow",
    "info": "green",
    "style": "green",
    "verbose": "green",
    "message": "bold",
    "source": None,
}


class Issue(Exception):
    def __init__(self, message: str, file: BinaryIO, obj: Any, line: int | None = None, print_obj=True):
        self.formatted_message = f"{message} in file {file.name!r}"
        if line is not None:
            self.formatted_message += f" on line {line+1}"
        if print_obj:
            self.formatted_message += f"\n\ttype: {type(obj)}, value: {obj!r}"

    def __str__(self) -> str:
        return self.formatted_message


class IncludeMode(enum.StrEnum):
    # doc string used for click -> \b disables re-wrapping
    """\b
    Determines what to do with includes:
    - error: Any include statement causes a failed check.
    - ignore: Ignore all include statements.
    - error-remote: Try to include local files only. Remote files will fail the check.
    - ignore-remote: Try to include local files only. Remote files are ignored.
    Downloading remote files is currently not possible.
    Template & project type includes are treated equivalent to remote files.
    The default behaviour is "ignore-remote", but this may change in the future!
    When reading from stdin, paths are relative to the current working directory. When reading files, they are relative to the file.
    Missing files will cause a failed check. Beware that no CI variable substitution takes place. Globs (*, **) are supported.
    """

    ERROR = "error"
    IGNORE = "ignore"
    ERROR_REMOTE = "error-remote"
    IGNORE_REMOTE = "ignore-remote"


class Checker:
    """
    Gitlab CI file shellcheck transformer.

    The only public parts of the API are the constructor and process function.
    """

    def __init__(self, cmd: list[str], includes: IncludeMode):
        self.cmd = cmd
        self.includes = includes
        self._file_stack = []  # Basic recursion detection

    def process(self, file: BinaryIO):
        """
        Process a gitlab-ci file (or stdin stream).
        The data must be valid and well-formed for proper functioning of this function.

        Raises or yields nothing if all is good.
        Fatal issues cause raised exceptions (invalid yaml etc)
        Other issues are yielded so they can be handled by the caller as needed.
        """
        self._file_stack.append(os.path.abspath(file.name))

        # Load the YAML file with round-trip loader, meaning it preserves comment & line nr info to allow dumping later.
        # We abuse this and the required "internals" to get the line nr information from the undocumented .lc attributes.
        # To get the line info for a dict entry, you need to use <parent>.lc.key(<name>)[0] (index 1 would be the column).
        # For an array entry, replace .key(<name>) with .item(<index>).
        # Beware: ruamel.yaml's data is 0 indexed, shellcheck is 1 indexed.
        yaml = ruamel.yaml.YAML(typ="rt")
        root = yaml.load(file)
        if not isinstance(root, CommentedMap):
            raise Issue("The given file root object is not a map", file, root)

        if INCLUDE in root:
            include = root[INCLUDE]
            if isinstance(include, str):
                yield from self.process_include(file, include, root.lc.item(INCLUDE)[0])
            elif isinstance(include, CommentedSeq):
                for idx, item in enumerate(include):
                    yield from self.process_include(file, item, include.lc.item(idx)[0])
            else:
                raise Issue(f"{INCLUDE!r} is not a string or list", file, root[INCLUDE], root.lc.key(INCLUDE)[0])

        for job_name, job_data in root.items():
            # Do not skip over templates (.-prefixed) or defaults, then we don't have to do inheritance later.
            if job_name in GLOBAL_KEYWORDS:
                if "script" in job_name:
                    # Special case: We don't really have a job name, and the job_data is actually the root object.
                    yield from self.process_section(job_name, file, "globally defined (deprecated!)", root, root[job_name])
                continue
            if not isinstance(job_data, CommentedMap):
                raise Issue(f"Job {job_name!r} object is not a map", file, job_data, root.lc.key(job_name)[0])
            LOG.debug("Processing job %r", job_name)

            if seq := job_data.mlget(["hooks", "pre_get_sources_script"]):
                yield from self.process_section("hooks:pre_get_sources_script", file, job_name, job_data, seq)
            if seq := job_data.get("before_script"):
                yield from self.process_section("before_script", file, job_name, job_data, seq)
            if seq := job_data.get("script"):
                yield from self.process_section("script", file, job_name, job_data, seq)
            if seq := job_data.get("after_script"):
                yield from self.process_section("after_script", file, job_name, job_data, seq)

        self._file_stack.pop()

    def process_section(self, key: str, file: BinaryIO, job_name: str, job_data: CommentedMap, seq: CommentedSeq) -> Iterator[str]:
        """
        Process a section of a file
        :param key: key of the data we're handeling (after_script, script, before_script, hooks:pre_get_sources_script)
        :param file: file object
        :param job_name: name of the job, used for display only
        :param job_data: the job object (aka the parent in which we can find the key), used to extract line numbers
        :param seq: the script sequence, type checking done internally
        """
        LOG.debug("Processing %s", key)
        # Make some assertions about the data types. A section must be a CommentedSeq[str] as that retains line nr info.
        if not isinstance(seq, CommentedSeq):
            raise Issue(f"Job {job_name!r} {key} object is not a sequence", file, seq, job_data.lc.key(key)[0])
        for idx, item in enumerate(seq):
            if not isinstance(item, str):
                raise Issue(f"Job {job_name!r} {key} entry {idx+1} is not a string", file, item, seq.lc.item(idx)[0])

        # OK now we're reasonably sure that every item in the script sequence is at least a str derivative
        # Now we concat the entire thing and hand it to shellcheck and parse it's json output.
        # It would be simpler to check every item individually, but that isn't how it works when running.
        # The json1 output format is not properly documented.
        LOG.debug("Merged script, as passed to shellcheck:\n%s", "\n".join(seq))
        result = subprocess.run(self.cmd, input="\n".join(seq), text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # 0 means no issues found, so we can return early without yielding any issues.
        if result.returncode == 0:
            return

        # Shellcheck has some remarks, let the fun begin.
        issues = json.loads(result.stdout)["comments"]
        # Sort here based on line number, so we can handle the issues sequentially and guarantee we don't skip lines that need comments
        # Within a line we sort based on reverse column so the first issues text doesn't overlap with the position idicator bar for subsequent issues.
        issues.sort(key=lambda x: (x["line"], -x["column"]))
        LOG.debug("Issues: %r", issues)

        yield click.style(
            f"Issue(s) in job {job_name!r} {key} in file {file.name!r} with merged script (line numbers are estimates):", fg="red"
        )

        # We'd like to accurately report the line nr of the issue, but yaml is !fun! when it comes to strings.
        # https://yaml-multiline.info/
        # So the joined script we passed to shellcheck isn't likely to look like the yaml file.
        # Thus, we need line accounting.

        # This bit of magic allows us to iterate over the issues outside a for/while loop, since we only want to go to the next once
        # we've done processing it, which may take any number of lines in the script to happen.
        issue_iterator = iter(issues)
        i = next(issue_iterator)

        # Line number as passed to ShellCheck. Incremented for every line in the merged output.
        # Not shown to user, because it bears no direct relation to the line nr in the yml file.
        # Required to match up issues with their respective lines in the ShellScript input.
        script_line_nr = 0

        # Every item in seq is a string. They are all joined by newlines into the script gitlab runs, but we can't just glue then if we
        # want accurate line numbers from the yaml file because there are many different forms of yaml multiline strings.
        # In a simpler world, every item would be a single line of shell code and it would be easy, but it's not.
        item: str
        for idx, item in enumerate(seq):
            # Line number of the start of this item in the script array.
            source_line = seq.lc.item(idx)[0]
            # If this is a "Literal Scalar" style string (- |\n...), the actual string starts only on the next line, so +1
            # "Folded Scalar" styles strings (- >) fold the newlines into spaces, which messes up our tracking.
            # This is ignored since they are far less common in scripts and handling it would require significant added complexity.
            # Chomping (strip -, clip or keep +) of newlines only affects newlines at the end of the script, so we don't care here.
            # Multiline quoted strings are undetectable and may cause issues with line number accounting.
            if isinstance(item, LiteralScalarString):
                source_line += 1

            line: str
            # .split(\n) instead of .splitlines because we need to get an entry for every line, including empty last lines.
            for line_index, line in enumerate(item.split("\n")):
                # pre-increment because it keeps the code together and the first line must start at 1 anyway.
                script_line_nr += 1
                # items in the script sequence are merged with newlines, so add 1 to account for the extra line.
                yml_line = source_line + line_index + 1

                yield f'{click.style(f"{yml_line:4} │", fg="cyan")} {line}'
                # As long as the current issue (incremented at the bottom of the while) is related to the current line:
                while i["line"] == script_line_nr:
                    prefix_len = 6
                    # Inclusive numbering, so -2 to get only the parts between the corner bits.
                    # If we're taling about a single character, we'll end up printing a 2 wide indicator. Oh well.
                    bar = "─" * max(0, i["endColumn"] - i["column"] - 2)
                    message = f'{i["level"]}: {i["message"]}'
                    # If it fits, print the mess age before the position bar to keep the overal line lengt sane (prevents hard-wraps)
                    if i["column"] < len(message):
                        indent = " " * (i["column"] + prefix_len)
                        comment = click.style(f"{indent}└{bar}┘ {message}", fg=COLORS.get(i["level"]))
                    else:
                        indent = " " * (i["column"] - len(message) - 2)  # -2 to account for 2 spaces in f-string
                        comment = click.style(f'{" " * prefix_len} {message}{indent} └{bar}┘', fg=COLORS.get(i["level"]))
                    yield comment
                    # Go to the next issue or exit the while loop if there are none left.
                    # We don't have to exit the for loop(s) because i[line] will never be == script_line_nr anymore,
                    # so we'll never enter the while after the last indicator anymore.
                    # By not exiting the for we still print the rest of the script without needing additional special logic.
                    try:
                        i = next(issue_iterator)
                    except StopIteration:
                        # If there are not more issues, we can stop processing this while loop.
                        break
                # todo: Compute fix suggestion. Effort abandoned due to extensive processing required.
                #   The fix array contains a list of operations to do on the original line, but they also all
                #   have influence on the output line, so it's not so easy to just apply them sequentially.

    def process_include(self, file: BinaryIO, item: str | dict[str, Any], item_line_nr: int) -> Iterator[str]:
        """
        Includes are a complex beast. We only handle a limited subset of simple cases.
        Docs & examples: https://docs.gitlab.com/ee/ci/yaml/includes.html & https://docs.gitlab.com/ee/ci/yaml/index.html#include
        """
        # Turn string into correct object, for simpler handling later.
        if isinstance(item, str):
            # noinspection HttpUrlsUsage
            if item.startswith("https://") or item.startswith("http://"):
                item = {"remote": item}
            else:
                item = {LOCAL: item}

        match self.includes:
            case IncludeMode.ERROR:
                raise Issue("Including other files is not supported", file, item, item_line_nr)
            case IncludeMode.IGNORE:
                LOG.debug("Ignoring include %r", item)
                return
            case IncludeMode.ERROR_REMOTE:
                if LOCAL not in item:
                    raise Issue("Including remote files is not supported", file, item, item_line_nr)
            case IncludeMode.IGNORE_REMOTE:
                if LOCAL not in item:
                    LOG.debug("Ignoring remote include %r", item)
                    return
            case _:
                raise RuntimeError("Missing IncludeMode case!")

        if remote_keys := item.keys() & {"remote", "project", "template"}:
            remote_keys.add(LOCAL)
            keys = ", ".join(remote_keys)
            raise Issue(f"Single include has multiple types: {keys}", file, item, item_line_nr)

        LOG.debug("Processing local include %r", item)
        local = item[LOCAL]
        # May be false if the input was a single string, in that case we keep the item_line_nr we got from the caller.
        if isinstance(item, CommentedMap):
            item_line_nr = item.lc.item(LOCAL)[0]

        # Absolute paths don't exist in this context. Strip off leading characters until it isn't anymore
        while os.path.isabs(local):
            local = local[1:]

        root_dir = os.path.abspath(os.path.dirname(file.name))  # This also works with stdin, because dirname is '' which resolves to CWD.
        include_files = glob.glob(local, root_dir=root_dir, recursive=True, include_hidden=True)
        LOG.debug("Glob %r relative to %r: %r", local, root_dir, include_files)
        if not include_files:
            raise Issue("No matching file(s) to include", file, local, item_line_nr)

        for include_file in include_files:
            include_file = os.path.abspath(os.path.join(root_dir, include_file))
            # This check must happen here instead of in self.process to allow line number accounting
            if include_file in self._file_stack:
                raise Issue("Recursive file inclusion", file, include_file, item_line_nr)

            LOG.debug("Processing included file %r", include_file)
            with open(include_file, "rb") as f:
                yield from self.process(f)
