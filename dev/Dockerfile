FROM python:3.7

WORKDIR /app

COPY src .

RUN pip install -r requirements.txt

ENTRYPOINT [ "gunicorn",  "main:create_app"]