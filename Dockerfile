FROM python:3.11 AS base

WORKDIR /app

COPY requirements.txt /app
COPY entrypoint.sh /usr/bin
RUN chmod +x /usr/bin/entrypoint.sh

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt


FROM base AS application

COPY ./src /app

RUN rm requirements.txt

EXPOSE 3000

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "src.main:app", "--workers", "1", "--bind", "0.0.0.0:3000", "--timeout", "120", "--keep-alive", "5", "--max-requests", "1000", "--graceful-timeout", "30"]


FROM base AS test

COPY . /app

RUN pip install --no-cache-dir -r /app/requirements-dev.txt

RUN rm requirements.txt
RUN rm requirements-dev.txt
