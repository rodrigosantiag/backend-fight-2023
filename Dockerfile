FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11 AS base

WORKDIR /app

COPY requirements.txt /app
COPY entrypoint.sh /usr/bin
RUN chmod +x /usr/bin/entrypoint.sh

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt


FROM base AS application

COPY ./src /app

RUN rm requirements.txt

EXPOSE 3000

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "src.main:app", "--bind", "0.0.0.0:3000"]


FROM base AS test

COPY . /app

RUN pip install --no-cache-dir -r /app/requirements-dev.txt

RUN rm requirements.txt
RUN rm requirements-dev.txt
