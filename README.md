# Это проект  бэкенда для бронирования столов.
## В проекте используется FastAPI, SQLAlchemy, PostgreSQL(asyncpg), Docker, Docker-compose, Alembic, Pytest.
[Подровные условия задачи](Task.md)

[Roadmap](Roadmap.md)

# Для запуска:
## Локально с docker-compose
### Запустите compose
```
docker-compose up --build
```
OpenAPI [http://localhost:8080/docs]

или

OpenAPI [http://127.0.0.1:8080/docs]

### Запустите alembic в контейнере(применить все миграции)
```python
alembic upgrade head
```

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

## Alembic используется для миграций:
### 1. Создание миграции
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

# Структура проекта:
```

task_TableReservApi
├── alembic
│   ├── versions
│   │   └── cee5bd0fa609_init1.py
│   ├── env.py
│   ├── README
│   └── script.py.mako
├── app
│   ├── alembic
│   ├── api
│   │   └── v1
│   │       └── routers
│   │           └── reservations.py
│   │           └── routers.py
│   │           └── tables.py
│   ├── core
│   │   ├── config.py
│   │   └── logger.py
│   │
│   ├── database
│   │   └── db.py
│   ├── main
│   │   └── app.py
│   ├── models
│   │   ├── Base.py
│   │   ├── Reservations.py
│   │   └── Tables.py
│   ├── schema
│   │   ├── Reservation.py
│   │   └── Table.py
│   ├── services
│   │   ├── expt.py
│   │   ├── ReservTableService.py
│   │   └── TableService.py
│   ├── utils
│   │   └── patterns
│   │       ├── rep
│   │       │   ├── repository.py
│   │       │   ├── ReservationRepository.py
│   │       │   └── TableRepository.py
│   │       └── uow
│   │           └── UnitOfWork.py
│   ├── config.py
│   ├── logger.py
│   └── requirements.txt
│   
├── test
│   ├── func_tests
│   └── unit_tests
│       ├── models_test.py
│       ├── repository_test.py
│       ├── schemas_test.py
│       ├── services_test.py
│       └── uof_test.py
├── .dockerignore
├── .ENV
├── .ENV.EAMPLE
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── pytest.ini
├── README.md
├── roadmap.md
└── Task.md
```