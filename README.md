#api_yamdb
CI/CD для проекта API YAMDB

## Технологический стек
[![Django-app workflow](https://github.com/DeffronMax/yamdb_final/actions/workflows/main.yml/badge.svg)](https://github.com/DeffronMax/yamdb_final/actions/workflows/main.yml)
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=008080)](https://www.postgresql.org/)
[![JWT](https://img.shields.io/badge/-JWT-464646?style=flat&color=008080)](https://jwt.io/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=56C0C0&color=008080)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=56C0C0&color=008080)](https://gunicorn.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/products/docker-hub)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat&logo=GitHub%20actions&logoColor=56C0C0&color=008080)](https://github.com/features/actions)


С использованием Continuous Integration и Continuous Deployment.
При пуше в ветку main автоматически отрабатывают сценарии:
1. Автоматический запуск тестов,
2. Обновление образов на Docker Hub,
3. Автоматический деплой на боевой сервер,
4. Отправка сообщения в телеграмм-бот в случае успеха.

##Запуск проекта:

Сначала нужно клонировать репозиторий и перейти в корневую папку:
```
git clone git@github.com:TretyakovAnton/yamdb_final.git
cd yamdb_final
```
Затем нужно перейти в папку yamdb_final/infra и создать в ней файл .env с 
переменными окружения, необходимыми для работы приложения.
```
cd infra/
touch .env
sudo nano .env
```

Пример содержимого файла:
```
SECRET_KEY=key
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

## Подготовка удаленного сервера для развертывания приложения

Для работы с проектом на удаленном сервере должен быть установлен Docker и docker-compose.
Установка docker:
```
sudo curl -fsSL https://get.docker.com -o get-docker.sh
```
Запуск docker:
```
sh get-docker.sh
```
Установка docker-compose:
```
sudo apt install docker-compose
```
Скопируйте файлы docker-compose.yaml и папку nginx:





##Подготовка репозитория на GitHub

Для использования Continuous Integration и Continuous Deployment необходимо в репозитории на GitHub прописать Secrets - переменные доступа к вашим сервисам.
Переменые прописаны в workflows/yamdb_workflow.yaml
```
DOCKER_PASSWORD, DOCKER_USERNAME - для загрузки и скачивания образа с DockerHub 
USER, HOST, PASSPHRASE, SSH_KEY - для подключения к удаленному серверу 
TELEGRAM_TO, TELEGRAM_TOKEN - для отправки сообщений в Telegram
```


## После каждого обновления репозитория (`git push`) будет происходить:
1. Проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8) и запуск pytest из репозитория yamdb_final
2. Сборка и доставка докер-образов на Docker Hub.
3. Автоматический деплой.
4. Отправка уведомления в Telegram.

Далее следует запустить docker-compose: 
```
docker-compose up -d --build
```
Будут созданы и запущены в фоновом режиме необходимые для работы приложения 
контейнеры (db, web, nginx).

Затем нужно внутри контейнера web выполнить миграции, создать 
суперпользователя и собрать статику:
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input 
```



##Остановка контейнеров

Для остановки работы приложения можно набрать в терминале команду Ctrl+C 
либо открыть второй терминал и воспользоваться командой
```
docker-compose stop 
```
Также можно запустить контейнеры без их создания заново командой
```
docker-compose start 
```

##Бэйдж
https://github.com/TretyakovAnton/yamdb_final/workflows/yamdb_workflow.yaml/badge.svg

## Примеры запросов:

1. POST-запрос создание пользователя на эндпоинт /api/v1/auth/signup/
```
{
    "email": "string",
    "username": "string"
}
```
После чего получает ответ на указанный email с кодом подтверждения (confirmation_code)

2. ПPOST-запрос получения токена на эндпоинт /api/v1/auth/token/.
Пример POST-запроса:
```
{
    "username": "string",
    "confirmation_code": "string"
}
```

В ответе на запрос ему приходит token (JWT-токен).

Пример ответа:
```
{
    "token": "string",
}
```

3. PATCH-запрос изменения информации о себе на эндпоинт /api/v1/users/me/.
Пример POST-запроса:
```
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string"
}
```

Пример ответа:
```
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
```

4. Просмотр и создание объектов на эндпоинт /api/v1/titles/:

Пример GET-запроса:
```
[
    {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": []
    }
] 
```

Пример Post-запроса (доступно только админу, суперюзеру):
```
{
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": [
        "string"
    ],
    "category": "string"
}
```


##Документация в формате Redoc:

Чтобы посмотреть документацию API в формате Redoc, нужно локально запустить 
проект и перейти на страницу http://127.0.0.1:8000/redoc/