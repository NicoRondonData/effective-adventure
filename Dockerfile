FROM python:3.9-alpine

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /code/requirements.txt

RUN apk add build-base
RUN apk add postgresql-libs && \
  apk add --no-cache gcc musl-dev postgresql-dev && \
  pip install -r /code/requirements.txt && \
  rm -rf /var/cache/apk/*


COPY ./app /code/app
#COPY ./cli /code/cli
#COPY ./migrations /code/migrations
#COPY ./tests /code/tests
#COPY ./alembic.ini /code/alembic.ini
#COPY ./docker-compose.yaml /code/docker-compose.yaml



CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8042", "--reload"]
