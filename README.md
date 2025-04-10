# Это проект  бэкенда для бронирования столов.
## В проекте используется FastAPI, SQLAlchemy, PostgreSQL, Docker, Docker-compose, Alembic, Pytest.
## Alembic используется для миграций:
### 1. Создание 1 файла миграции
```
alembic revision --autogenerate -m "init"
```
### 2. Применить миграции
```
alembic upgrade head
```
### 3. Откатить миграции
```
alembic downgrade
```
# Для запуска:
## Локально с docker-compose
### Запустите compose
```
docker-compose up --build
```
OpenAPI [http://localhost:8080/docs]
или
OpenAPI [http://127.0.0.1:8080/docs]

## Локально без docker-compose
### 1. Установите venv 
```python
python -m venv .venv
```
### 2. Установите зависимости
```python
python -m pip install -r app\requirements.txt
```
### 3. Запустите проект
Выполните комманду в корне проекта
```python
python -m uvicorn  app.main.app:app --host localhost  --port 8080 --reload
```
