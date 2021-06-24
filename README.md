# Foodgram
Проект «Продуктовый помощник».
Это онлайн-сервис, где пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

# Стек технологий
1. Автоматизация и тестирование:
- github actions, pytest
2. Сборка и хранение:
- docker, docker-compose, docker-hub
3. Хостинг:
- Яндекс Облако
4. Логгирование:
- Telegram API

Контейнеры:
1. Web:
    - Python + Django REST Framework
    - Django-filter - фильтрация запросов
    - Git - система контроля версий
    - Javascript + HTML - фронтенд
2. Nginx
3. Postgresql

# Установка
1. Клонирйте репозиторий с проектом
```sh
git clone https://github.com/ne4istii/foodgram.git
```
2. Подготовить удаленный сервер для работы:
- Установите docker:
```sh
sudo apt install docker.io 
```
- Установите [docker-compose](https://docs.docker.com/compose/install/):
```sh
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
- Скопируйте подготовленные файлы docker-compose.yaml и nginx/default.conf из вашего проекта на сервер в home/<ваш_username>/docker-compose.yaml и home/<ваш_username>/nginx/default.conf соответственно.
- Добавьте в Secrets GitHub Actions переменные окружения
3. При пуше в ветку main код автоматически деплоится на сервер

# Доступ к проекту
- http://ne4istii.tk/
- Автор: [ne4istii](https://github.com/ne4istii)

![foodgram_workflow Actions Status](https://github.com/ne4istii/foodgram/actions/workflows/foodgram_workflow.yaml/badge.svg)
