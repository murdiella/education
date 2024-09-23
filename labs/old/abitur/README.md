# Личный кабинет абитуриента

## Разработчикам

### Локальный запуск проекта

#### При помощи `docker-compose`

1. Склонировать проект:

`git clone [URL] [DIR]`

2. Перейти в директорию проекта

`cd [DIR]`

3. Скопировать окружение разработчика в текущее окружение:

`cp environments/.env.development .env`

4. Запустить проект:

`docker-compose up`

5. Проект должен быть доступен по `localhost:80`