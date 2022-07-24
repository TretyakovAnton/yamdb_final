FROM python:3.7-slim

WORKDIR /app

ENV APP_HOME=/usr/src/web

COPY . .

RUN python -m pip install --upgrade pip
WORKDIR /app/api_yamdb
RUN pip3 install -r requirements.txt --no-cache-dir




WORKDIR $APP_HOME
COPY . $APP_HOME

CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000