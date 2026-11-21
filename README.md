# library_catalog

REST API для управления библиотечным каталогом. Проект разработан на Python с использованием FastAPI, SQLAlchemy 2.x и PostgreSQL.

Приложение предоставляет CRUD-операции для книг, поиск с фильтрацией и пагинацией, а также интеграцию с Open Library API для автоматического обогащения информации о книгах.

## Возможности

- Создание, получение, обновление и удаление книг.
- Поиск книг по названию и автору.
- Фильтрация по жанру, году издания и доступности.
- Пагинация результатов.
- Проверка уникальности ISBN.
- Валидация данных на уровне API и бизнес-логики.
- Автоматическое получение дополнительной информации из Open Library.
- Обработка ошибок и исключений.
- Проверка состояния приложения и подключения к базе данных.
- Автоматическая документация API через Swagger UI и ReDoc.

## Технологический стек

- **Python 3.11+**
- **FastAPI** — REST API.
- **SQLAlchemy 2.x** — ORM и асинхронная работа с БД.
- **PostgreSQL 16** — база данных.
- **Alembic** — миграции базы данных.
- **Pydantic v2** — валидация данных и настройки.
- **Pydantic Settings** — конфигурация приложения.
- **Poetry** — управление зависимостями.
- **Docker Compose** — запуск PostgreSQL.
- **HTTPX** — асинхронные HTTP-запросы к Open Library.
- **Ruff, Black, Mypy** — проверка качества и типизации кода.
- **Pytest** — тестирование.

## Архитектура проекта

Проект построен на основе многослойной архитектуры с разделением ответственности:

- **API Layer** — HTTP-эндпоинты, схемы запросов и ответов, зависимости.
- **Domain Layer** — бизнес-логика, сервисы, исключения и мапперы.
- **Data Layer** — ORM-модели, репозитории и работа с базой данных.
- **External Layer** — интеграция с внешними API.

### Структура проекта

```text
library_catalog/
├── src/
│   └── library_catalog/
│       ├── api/
│       │   ├── dependencies.py
│       │   └── v1/
│       │       ├── routers/
│       │       └── schemas/
│       ├── core/
│       │   ├── config.py
│       │   ├── database.py
│       │   ├── exceptions.py
│       │   └── logging_config.py
│       ├── data/
│       │   ├── models/
│       │   └── repositories/
│       ├── domain/
│       │   ├── exceptions.py
│       │   ├── mappers/
│       │   └── services/
│       ├── external/
│       │   ├── base/
│       │   └── openlibrary/
│       ├── utils/
│       └── main.py
├── alembic/
│   └── versions/
├── tests/
├── .env.example
├── docker-compose.yml
├── alembic.ini
├── pyproject.toml
├── poetry.lock
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

### 3. Настройка переменных окружения

Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

Пример конфигурации:

```env
ENVIRONMENT=development
DEBUG=true
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/library_catalog
API_V1_PREFIX=/api/v1
```

При необходимости измените параметры подключения к базе данных.

### 4. Запуск PostgreSQL

Для запуска базы данных используйте Docker Compose:

```bash
docker compose up -d
```

Проверить состояние контейнера:

```bash
docker compose ps
```

### 5. Применение миграций

Из корневой директории проекта выполните:

```bash
poetry run alembic upgrade head
```

### 6. Запуск приложения

```bash
poetry run uvicorn library_catalog.main:app --reload
```

После запуска приложение будет доступно по адресу:

`http://127.0.0.1:8000`

## API Endpoints

Все основные эндпоинты расположены под префиксом `/api/v1`.

| Метод | Endpoint | Описание |
|---|---|---|
| GET | `/` | Корневой эндпоинт |
| POST | `/api/v1/books/` | Создание книги |
| GET | `/api/v1/books/` | Получение списка книг |
| GET | `/api/v1/books/{book_id}` | Получение книги по UUID |
| PATCH | `/api/v1/books/{book_id}` | Частичное обновление книги |
| DELETE | `/api/v1/books/{book_id}` | Удаление книги |
| GET | `/api/v1/health/` | Проверка состояния приложения и БД |

### Фильтрация и пагинация

Для получения списка книг поддерживаются следующие query-параметры:

| Параметр | Описание |
|---|---|
| `title` | Поиск по названию (частичное совпадение, без учёта регистра) |
| `author` | Поиск по автору (частичное совпадение, без учёта регистра) |
| `genre` | Точное совпадение по жанру |
| `year` | Точный год издания |
| `available` | Фильтр по доступности (`true` / `false`) |
| `page` | Номер страницы, начиная с 1 |
| `page_size` | Количество книг на странице (от 1 до 100, по умолчанию 20) |

Пример запроса:

```http
GET /api/v1/books/?title=Python&available=true&page=1&page_size=10
```

## Интеграция с Open Library

При создании книги приложение может обращаться к Open Library API для получения дополнительной информации.

Поддерживается поиск по ISBN и названию с автором.

Полученные данные могут включать:

- Обложку книги.
- Темы и категории (subjects).
- Издателя.
- Рейтинг.
- Дополнительное описание и сведения о книге.

Если внешний сервис недоступен, создание книги не блокируется: приложение продолжает работу с переданными данными.

## Документация API

После запуска приложения доступны:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc
- **OpenAPI JSON:** http://127.0.0.1:8000/openapi.json

## Проверка качества кода

Проверка кода с помощью Ruff:

```bash
poetry run ruff check src/library_catalog/
```

Проверка типизации:

```bash
poetry run mypy src/library_catalog/
```

Проверка форматирования:

```bash
poetry run black --check src/library_catalog/
```

Форматирование кода:

```bash
poetry run black src/library_catalog/
```

## Миграции базы данных

Создание новой миграции:

```bash
poetry run alembic revision --autogenerate -m "migration description"
```

Применение миграций:

```bash
poetry run alembic upgrade head
```

Просмотр текущей версии:

```bash
poetry run alembic current
```

## Статус проекта

Проект находится в стадии разработки в рамках практического изучения Python Backend Development.