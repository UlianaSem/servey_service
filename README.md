# Survey service

## Описание проекта

Веб-приложение на базе Django для проведения опросов и возможностью динамического отображения вопросов в зависимости от ответов пользователя. 

## Технологии

- Linux
- Python
- Poetry
- Django
- PostgreSQL
- Docker
- Docker Compose

## Зависимости

Зависимости, необходимые для работы проекта, указаны в файле pyproject.toml.

## Как запустить проект

Для запуска проекта необходимо выполнить следующие шаги:
1. При необходимости установите Docker и Docker Compose на компьютер с помощью инструкции https://docs.docker.com/engine/install/
2. Cклонируйте репозиторий себе на компьютер
3. Создайте файл .env и заполните его, используя образец из файла .env.example
4. Соберите образ с помощью команды `docker-compose build`
5. Запустите контейнеры с помощью команды `docker-compose up`

## Файл .env.example

1. `DATABASES_NAME, DATABASES_USER, DATABASES_PASSWORD, DATABASES_HOST` - данные для подключения к БД
2. `SECRET_KEY, DEBUG, ALLOWED_HOSTS`

## Тестовые пользователи

1. `email=admin@admin.ru`

    `password=admin`

2. `test@testov.ru`

    `password=test1test`

## Авторы

UlianaSem

## Связь с авторами

https://github.com/UlianaSem/
