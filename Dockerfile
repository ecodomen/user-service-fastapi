FROM python:3.11-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./alembic.ini /code/alembic.ini

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
