FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
 build-essential \
 libpq-dev \
 ca-certificates \
 netcat-traditional

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt

RUN python3 -m pip install --upgrade pip

RUN pip install -r /tmp/requirements.txt

EXPOSE 7000