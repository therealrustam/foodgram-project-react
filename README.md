![Foodgram](https://github.com/therealrustam/foodgram-project-react/actions/workflows/main.yml/badge.svg)

# Проект Foodgram


## Адрес

http://foodgram.serveblog.net


## Описание

Cайт Foodgram - онлайн-сервис, на котором пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Пользовательские роли

- Гость (неавторизованный пользователь) — .
- Авторизованный пользователь — .
- Администратор — .

## Ресурсы API YaMDb

- Ресурс auth: аутентификация.
- Ресурс users: пользователи.
- Ресурс .

 ## Установка

В приложения настроено Continuous Integration и Continuous Deployment:
- автоматический запуск тестов,
- обновление образов на Docker Hub,
- автоматический деплой на боевой сервер при пуше в главную ветку main.

## Шаблон наполнения env-файла

DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД 

## Создание образа

Запустите терминал. Убедитесь, что вы находитесь в той же директории, где сохранён Dockerfile, и запустите сборку образа:
docker build -t foodgram .  
build — команда сборки образа по инструкциям из Dockerfile.
-t foodgram — ключ, который позволяет задать имя образу, а потом и само имя.
. — точка в конце команды — путь до Dockerfile, на основе которого производится сборка..

## Развёртывание проекта в нескольких контейнерах

Инструкции по развёртыванию проекта в нескольких контейнерах пишут в файле docker-compose.yaml. 
Убедитесь, что вы находитесь в той же директории, где сохранён docker-compose.yaml и запустите docker-compose командой docker-compose up. У вас развернётся проект, запущенный через Gunicorn с базой данных Postgres.

## Примеры

Примеры запросов по API:

- [GET] /api// - Получить список всех .



## Авторы

Рустам Вахитов
