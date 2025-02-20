#checkov:skip=CKV_DOCKER_2: Healthchecks are not the responsibility of Docker, we have ECS/ELB for that
# Build image
FROM python:3.11.9-slim-bookworm as python-build
RUN useradd -m nonrootuser
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_PATH=/home/nonrootuser/.local \
    VENV_PATH=/home/nonrootuser/venv
ENV PATH="$POETRY_PATH/bin:$VENV_PATH/bin:$PATH"
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y -o Dpkg::Options::="--force-confold" \
    curl \
    gcc
USER nonrootuser
    # install poetry - uses $POETRY_VERSION internally
RUN curl -sSL https://install.python-poetry.org | python3 - \
    # configure poetry & make a virtualenv ahead of time since we only need one
    && python -m venv $VENV_PATH \
    && python -m pip install --upgrade pip \
    && poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml ./
RUN . $VENV_PATH/bin/activate \
    && poetry install --no-interaction --no-ansi --only main -vvv

# Runtime image
FROM python:3.11.9-slim-bookworm as runtime
RUN useradd -m nonrootuser
ENV VENV_PATH=/home/nonrootuser/venv \
    PATH="/home/nonrootuser/venv/bin:$PATH" \
    PYTHONPATH=/app
WORKDIR /app
RUN chown -R nonrootuser:nonrootuser /app
COPY --from=python-build --chown=nonrootuser:nonrootuser $VENV_PATH $VENV_PATH
# COPY --from=python-build --chown=nonrootuser:nonrootuser /builds /builds
COPY --chown=nonrootuser:nonrootuser . ./
EXPOSE 8090
ENV WORKER_TYPE="uvicorn.workers.UvicornWorker" \
    WORKER_NUM=1 \
    THREAD_NUM=1
USER nonrootuser
CMD uvicorn src.main:app --host 0.0.0.0 --port 8090
