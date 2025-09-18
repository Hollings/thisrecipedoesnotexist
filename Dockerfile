# syntax=docker/dockerfile:1
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install build dependencies for bcrypt and create volume target dir
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libffi-dev \
    && mkdir -p /data \
    && rm -rf /var/lib/apt/lists/*

COPY python_server/requirements.txt ./python_server/requirements.txt
RUN pip install --upgrade pip \
    && pip install -r python_server/requirements.txt

COPY python_server ./python_server

EXPOSE 8000

ENV FLASK_APP=python_server.app \
    PYTHONPATH=/app

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "python_server.app:create_app()"]
