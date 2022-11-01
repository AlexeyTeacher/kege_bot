# kege_bot
Телеграм бот для подготовки к ЕГЭ по информатики

Переменные окружения смотрите в `config.py`


### START Postgres
```bash
docker stop kege_db || true && \
docker rm kege_db || true && \
docker run -d --name kege_db --restart always -p 5580:5432  \
     -e POSTGRES_DB=kege \
     -e POSTGRES_USER=kege \
     -e POSTGRES_PASSWORD=kege \
     postgres -c shared_buffers=256MB 
```