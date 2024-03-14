FROM python:3.12.0-alpine
RUN apk add --no-cache build-base unixodbc-dev

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY . /app