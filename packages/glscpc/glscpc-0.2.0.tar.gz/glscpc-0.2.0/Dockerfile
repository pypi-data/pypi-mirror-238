FROM python:3.11-slim

ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1


# Allow caching of apt packages on host, if later RUN steps use the --mount options
RUN rm -f /etc/apt/apt.conf.d/docker-clean; echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache

# System dependencies
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update \
    && apt-get install -y shellcheck

# Prepare our work dir
WORKDIR /opt/glscpc
COPY dist dist

# Install the most recently generated .whl file in dist & delete the folder.
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade --upgrade-strategy eager "$(find dist -name '*.whl' | head -n1)" && rm -rf dist

ENTRYPOINT []
CMD ["glscpc"]
