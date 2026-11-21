# library_catalog

REST API для управления библиотечным каталогом. Проект разработан на Python с использованием FastAPI, SQLAlchemy и PostgreSQL.

## Технологический стек

- Python 3.11+
- FastAPI
- SQLAlchemy 2.x
- PostgreSQL 16
- Alembic
- Pydantic v2
- Poetry
- Docker Compose
- HTTPX
- Pytest
- Ruff, Black, Mypy

## Структура проекта

```text
library_catalog/
├── src/
│   └── library_catalog/
│       ├── api/          # API-слой
│       ├── core/         # Конфигурация и инфраструктура
│       ├── data/         # Модели и репозитории
│       ├── domain/       # Бизнес-логика
│       ├── external/     # Внешние API
│       ├── utils/        # Вспомогательные функции
│       └── main.py       # Точка входа приложения
├── alembic/              # Миграции базы данных
├── tests/                # Тесты
├── .env.example          # Пример переменных окружения
├── docker-compose.yml    # Конфигурация PostgreSQL
├── alembic.ini
├── pyproject.toml
└── README.md
```

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone git@github.com:jezuzjevil/library_catalog.git
cd library_catalog
```

### 2. Установка зависимостей

```bash
poetry install
```

### 3. Настройка окружения

Создайте файл `.env` на основе примера:

```bash
cp .env.example .env
```

При необходимости измените значения переменных окружения.

### 4. Запуск PostgreSQL

```bash
docker compose up -d
```

### 5. Применение миграций

```bash
poetry run alembic upgrade head
```

### 6. Запуск приложения

```bash
poetry run uvicorn library_catalog.main:app --reload
```

После запуска документация API доступна по адресу:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Health check: http://127.0.0.1:8000/health

## Конфигурация

Основные настройки приложения задаются через переменные окружения. Пример находится в `.env.example`.

## Разработка

Для запуска тестов:

```bash
poetry run pytest
```

Для проверки кода с помощью Ruff:

```bash
poetry run ruff check .
```

Для форматирования кода:

```bash
poetry run black .
```

## Статус проекта

Проект находится в разработке. Функциональность и структура расширяются по мере выполнения учебных заданий.