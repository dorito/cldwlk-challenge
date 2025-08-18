FROM python:3.13-alpine

ENV PYTHONUNBUFFERED=1

RUN pip install poetry

WORKDIR /code
COPY poetry.lock pyproject.toml /code/

RUN poetry config virtualenvs.create false && poetry install $(test "$APP_ENV" == production && echo "--only=main") --no-interaction --no-ansi --no-root
COPY . /code
