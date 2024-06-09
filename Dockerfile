FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11 AS base

WORKDIR /app

COPY requirements.txt /app
COPY prestart.sh /app
RUN chmod +x /usr/bin/entrypoint.sh

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt


FROM base AS application

COPY ./src /app/src

RUN rm requirements.txt

EXPOSE 3000

FROM base AS test

COPY . /app

RUN pip install --no-cache-dir -r /app/requirements-dev.txt

RUN rm requirements.txt
RUN rm requirements-dev.txt
