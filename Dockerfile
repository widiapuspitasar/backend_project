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

CMD ["/.venv/Scripts/gunicorn", "-w 4", "-b 0.0.0.0:5000", "app:app"]


