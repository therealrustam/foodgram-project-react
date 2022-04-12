![Yamdb](https://github.com/therealrustam/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

# Проект Foodgram


## Адрес

http://foodgram.serveblog.net


## Описание

Cайт Foodgram - онлайн-сервис, на котором пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Пользовательские роли

- Гость (неавторизованный пользователь) — может просматривать описания рецептов.
- Авторизованный пользователь — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.
- Администратор — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.

## Ресурсы API YaMDb

- Ресурс auth: аутентификация.
- Ресурс users: пользователи.
- Ресурс titles: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
- Ресурс categories: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
- Ресурс genres: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- Ресурс reviews: отзывы на произведения. Отзыв привязан к определённому произведению.
- Ресурс comments: комментарии к отзывам. Комментарий привязан к определённому отзыву.

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
docker build -t yamdb .  
build — команда сборки образа по инструкциям из Dockerfile.
-t yambd — ключ, который позволяет задать имя образу, а потом и само имя.
. — точка в конце команды — путь до Dockerfile, на основе которого производится сборка..

## Развёртывание проекта в нескольких контейнерах

Инструкции по развёртыванию проекта в нескольких контейнерах пишут в файле docker-compose.yaml. 
Убедитесь, что вы находитесь в той же директории, где сохранён docker-compose.yaml и запустите docker-compose командой docker-compose up. У вас развернётся проект, запущенный через Gunicorn с базой данных Postgres.

## Примеры

Примеры запросов по API:

- [GET] /api/v1//titles/{title_id}/reviews/ - Получить список всех отзывов.
- [POST]  /api/v1//titles/{title_id}/reviews/ - Добавить новый отзыв. Пользователь может оставить только один отзыв на произведение.
- [GET] /api/v1/titles/{title_id}/reviews/{review_id}/ - Получить отзыв по id для указанного произведения.
- [PATCH] /api/v1/titles/{title_id}/reviews/{review_id}/ - Частично обновить отзыв по id.
- [DELETE] /api/v1/titles/{title_id}/reviews/{review_id}/ - Удалить отзыв по id.


## Авторы

Рустам Вахитов
