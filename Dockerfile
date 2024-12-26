FROM python:3.13-slim

ARG POETRY_VERSION=1.8

ENV POETRY_HOME=/opt/poetry
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=1
ENV POETRY_VIRTUALENVS_CREATE=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_CACHE_DIR=/opt/.cache

RUN pip install "poetry==${POETRY_VERSION}"

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
COPY dam_k_server_hbbo_001/ dam_k_server_hbbo_001/
COPY dam_k_server_hbbo_001_cli/ dam_k_server_hbbo_001_cli/

RUN --mount=type=cache,target=$POETRY_CACHE_DIR,sharing=locked \
    poetry install

ENTRYPOINT [ "poetry", "run", "dam-k-server-hbbo-001" ]
