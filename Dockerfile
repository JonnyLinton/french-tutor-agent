# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# Install dependencies for sounddevice
RUN apt update
RUN apt upgrade -y
RUN apt install -y apt-utils
RUN apt install -y alsa-oss alsa-utils alsa-tools mpg123
RUN apt install -y libasound-dev
RUN uv pip install numpy
RUN apt install -y libportaudio2

# TODO: give docker access to the soundcard (currently this Dockerfile doesn't work)

# Copy the project files
ADD . /app

# Install project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

CMD ["uv", "run", "python", "src/main.py"]
