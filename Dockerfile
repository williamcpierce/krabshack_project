# pull official base image
FROM python:3.8.1-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2/pillow dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev zlib-dev jpeg-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./config/requirements.txt requirements.txt
RUN pip install -r requirements.txt

# set source
COPY ./src /src
WORKDIR /src