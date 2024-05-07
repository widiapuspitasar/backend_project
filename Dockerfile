# Use the official Python image as a base image
FROM python:3.9-slim

COPY . /app
WORKDIR /app

ARG DB_USERNAME
ARG DB_PASSWORD
ARG DB_HOST
ARG DB_NAME
ARG DB_USERNAME
ARG SECRET_KEY

RUN echo $DB_USERNAME
RUN echo $DB_PASSWORD
RUN echo $DB_HOST
RUN echo $DB_NAME
RUN echo $DB_USERNAME
RUN echo $SECRET_KEY

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV VIRTUALENVS_IN_PROJECT=1 \
    VIRTUALENVS_CREATE=1 

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["\.venv\Lib\site-packages\gunicorn", "-w 4", "-b 0.0.0.0:5000", "app:app"]

# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

ARG FLASK_DEBUG
ARG FLASK_ENV
ARG DATABASE_TYPE
ARG DATABASE_HOST
ARG DATABASE_NAME
ARG DATABASE_PORT
ARG DATABASE_USER
ARG DATABASE_PASSWORD
ARG JWT_SECRET_KEY

RUN echo $FLASK_DEBUG
RUN echo $FLASK_ENV
RUN echo $DATABASE_TYPE
RUN echo $DATABASE_HOST
RUN echo $DATABASE_NAME
RUN echo $DATABASE_PORT
RUN echo $DATABASE_USER
RUN echo $DATABASE_PASSWORD
RUN echo $JWT_SECRET_KEY

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN poetry install

COPY . /app

RUN poetry run flask 

CMD ["/app/.venv/bin/gunicorn", "-w 4", "-b 0.0.0.0:5000", "app:app"]
