FROM python:3.11

WORKDIR /app

COPY requirements.txt /app

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src /app
COPY entrypoint.sh /usr/bin
RUN chmod +x /usr/bin/entrypoint.sh
RUN rm requirements.txt

EXPOSE 3000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]
