FROM python:3.7-slim

# Создать и сделать директорию /app рабочей директорией
WORKDIR /app

# Копируем  /api_yamdb в рабочую директорию образа
COPY . .

# Выполнить установку зависимостей внутри контейнера
RUN python -m pip install --upgrade pip
RUN pip3 install -r api_yamdb/requirements.txt --no-cache-dir

# Выполнить запуск сервера разработки при старте контейнера
CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000"]