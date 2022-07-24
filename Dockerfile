FROM python:3.7-slim

WORKDIR /app

COPY . .

RUN python -m pip install --upgrade pip
WORKDIR /api_yamdb
RUN pip3 install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000"]