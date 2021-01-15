FROM python:3.7

WORKDIR /app
COPY src .

RUN pip install -r requirements.txt

ENTRYPOINT [ "gunicorn", "-b", "0.0.0.0", "main:create_app()", "--reload", "--log-level=debug" ]