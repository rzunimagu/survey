FROM python:3.7.10-alpine3.12 as base

FROM base as builder
RUN apk --no-cache add gcc musl-dev postgresql-dev python3-dev
RUN python -m pip install --upgrade pip

WORKDIR /app/
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
EXPOSE 8000
