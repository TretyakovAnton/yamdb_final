#api_yamdb
api для проекта yatube, где хранятится инофрмация о произведениях.

С использованием Continuous Integration и Continuous Deployment.
При пуше в ветку main автоматически отрабатывают сценарии:
1. Автоматический запуск тестов,
2. Обновление образов на Docker Hub,
3. Автоматический деплой на боевой сервер,
4. Отправка сообщения в телеграмм-бот в случае успеха.

##Стэк технологий:

- Python 3.7
- Django
- DRF
- Simple-JWT
- PostgreSQL
- Docker
- nginx
- gunicorn.


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
Создайте папку проекта на удаленном сервере и скопируйте туда файлы docker-compose.yaml, Dockerfile, host.conf:
```
scp ./<FILENAME> <USER>@<HOST>:/home/<USER>/yamdb_final/
```

##Запуск приложения в контейнерах

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

##c Подготовка репозитория на GitHub

Для использования Continuous Integration и Continuous Deployment необходимо в репозитории на GitHub прописать Secrets - переменные доступа к вашим сервисам.
Переменые прописаны в workflows/yamdb_workflow.yaml

* DOCKER_PASSWORD, DOCKER_USERNAME - для загрузки и скачивания образа с DockerHub 
* USER, HOST, PASSPHRASE, SSH_KEY - для подключения к удаленному серверу 
* TELEGRAM_TO, TELEGRAM_TOKEN - для отправки сообщений в Telegram


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
После этого проект должен быть доступен по адресу http://localhost/. 

##Заполнение базы данных

Нужно зайти на на http://localhost/admin/, авторизоваться и внести записи 
в базу данных через админку.



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