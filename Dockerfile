FROM python:3.10-slim

WORKDIR meeting_app

ENV TZ="Europe/Moscow"

RUN pip install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1

COPY pyproject.toml .

RUN poetry install

COPY ./meeting_app .
