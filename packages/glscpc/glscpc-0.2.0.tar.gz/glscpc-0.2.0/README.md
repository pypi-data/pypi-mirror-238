# GitLab CI ShellCheck pre-commit hook

```
┏━╸╻  ┏━┓┏━╸┏━┓┏━╸
┃╺┓┃  ┗━┓┃  ┣━┛┃  
┗━┛┗━╸┗━┛┗━╸╹  ┗━╸
```

This is a small project to help with maintaining clean GitLab CI scripts.

## Supported

- [before_script](https://docs.gitlab.com/ee/ci/yaml/#before_script), [script](https://docs.gitlab.com/ee/ci/yaml/#script), [after_script](https://docs.gitlab.com/ee/ci/yaml/#after_script)
- [hooks:pre_get_sources_script](https://docs.gitlab.com/ee/ci/yaml/#hookspre_get_sources_script)

## Not Supported

- Importing external yml files

## Dependencies

**It's required to install [shellcheck](https://shellcheck.net) and make it available in $PATH.**

All Python dependencies (see pyproject.toml) are installed by pip when you install the package.

When setting up a development environment, use hatch to set up the dependencies. Running `hatch build` will do the heavy lifting for you.

For Pycham support run `hatch env run which python` and add its output as an "existing" virtualenv interpreter.

## Usage

This script should be run *after* you check that the yml file is [well-formed](https://github.com/pre-commit/pre-commit-hooks#check-yaml) and [valid](https://github.com/emmeowzing/gitlabci-lint-pre-commit-hook).

The intended use is via the provided hook in the repo:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: main
    hooks:
      # Check if all yaml files are well-formed
      - id: check-yaml
  - repo: https://github.com/bjd2385/pre-commit-gitlabci-lint
    rev: master
    hooks:
      # Linting API requires you set the project ID correctly and also have an API token configured in your environment!
      # You also should skip this step in the CI, since if it was invalid, the CI wouldn't be running anyway.
      - id: gitlabci-lint
        args: ['-p', '49052761']
  # This repo <3
  - repo: https://gitlab.com/Qteal/oss/gitlabci-shellcheck-precommit
    rev: main
    hooks:
      - id: glscpc
```

Run `pre-commit autoupdate` to replace the branch references with the latest tags.

But it's also possible to install the Python package in your environment and run the `glscpc` script.

You can install the package via [pypi](https://pypi.org/project/glscpc) (only tagged versions are pushed) or the [GitLab package registry](https://gitlab.com/Qteal/oss/gitlabci-shellcheck-precommit/-/packages) (includes dev builds).

Run `glscpc --help` for usage information.
