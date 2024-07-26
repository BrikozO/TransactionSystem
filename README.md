# Система транзакций
Стек - sqlalchemy, fastapi, postgresql, alembic, Docker, docker-compose
## Начальная инициализация
Скопируйте проект с помощью команды `git clone https://github.com/BrikozO/TransactionSystem.git`
### Инициализация через docker-compose
1. В корневой директории проекта создайте файл ".env.docker" со следующим содержимым:
```
SECRET_KEY=64b77cab0a24e98ede0a1a4ee7663cf3695bea338bf641f51d239a88c392def9
HASH_ALG=HS256
TOKEN_EXPIRE_RATE=60
#PostgresDB
POSTGRES_USER=transactionadmin
POSTGRES_PASSWORD=testpass1234
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=transactionsystem
```
3. Выполните команду `docker compose up -d --build`
4. Проинициализируйте миграции с помощью `docker compose -f docker-compose.yml exec web alembic upgrade head`
### Инициализация без docker compose
1. Выполните команду `pip install -r requirements.txt`
2. Проинициализируйте миграции с помощью `alembic upgrade head`
3. В корневой директории проекта создайте файл ".env" со следующим содержимым:
```
SECRET_KEY=64b77cab0a24e98ede0a1a4ee7663cf3695bea338bf641f51d239a88c392def9
HASH_ALG=HS256
TOKEN_EXPIRE_RATE=60
#PostgresDB
POSTGRES_USER=transactionadmin
POSTGRES_PASSWORD=testpass1234
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=transactionsystem
```
4. Запустите веб-сервер через консоль с помощью `uvicorn app.main:app --reload`
