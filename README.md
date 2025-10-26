# Funds Allocation API

FastAPI-приложение для управления финансовыми проектами

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0-green.svg)](https://fastapi.tiangolo.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4.0-red.svg)](https://sqlalchemy.org)

## Особенности

- **Полноценное API** для благотворительных проектов
- **Автоматическое распределение** пожертвований по проектам (FIFO)
- **JWT-аутентификация** пользователей
- **Интеграция с SQLAlchemy** (асинхронный режим)
- **Автоматические миграции** через Alembic
- **Полная документация** OpenAPI/Swagger

## Быстрый старт

### 1. Клонирование репозитория и установка зависимостей

```bash
git clone https://github.com/IlyaShaposhnikov/funds_allocation_system.git
py -3.9 -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Настройка окружения

Создайте файл `.env` в корне проекта:

```ini
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET_KEY=your-secret-key
FIRST_SUPERUSER_EMAIL=admin@example.com
FIRST_SUPERUSER_PASSWORD=password
```

Это позволит создать первого суперпользователя с заданными логином и паролем при первом запуске программы.

### 3. Запуск миграций

```bash
alembic upgrade head
```

### 4. Запуск приложения

```bash
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Документация API

После запуска доступны:

- Swagger UI: [/docs](http://127.0.0.1:8000/docs)
- ReDoc: [/redoc](http://127.0.0.1:8000/redoc)

## Технологии

- [FastAPI](https://fastapi.tiangolo.com) - Веб-фреймворк
- [SQLAlchemy 2.0](https://sqlalchemy.org) - ORM
- [Alembic](https://alembic.sqlalchemy.org) - Миграции БД
- [Pydantic](https://pydantic-docs.helpmanual.io) - Валидация данных
- [JWT](https://jwt.io) - Аутентификация

## Структура проекта

```
cat_charity_fund/
├── app/                   # Основной код приложения
│   ├── api/               # Роутеры FastAPI
│   ├── core/              # Настройки и конфиги
│   ├── crud/              # Репозитории для работы с БД
│   ├── models/            # Модели SQLAlchemy
│   ├── schemas/           # Pydantic-схемы
│   ├── services/          # Бизнес-логика
│   └── main.py            # Точка входа
├── alembic/               # Миграции БД
├── tests/                 # Тесты
├── requirements.txt       # Зависимости
└── README.md              # Этот файл
```

## Аутентификация

Система использует JWT-токены. Для доступа к защищенным эндпоинтам:

1. Авторизуйтесь через `/auth/jwt/login`
2. Используйте полученный токен в заголовке:
   ```
   Authorization: Bearer ваш-токен
   ```

## Автор
Илья Шапошников
ilia.a.shaposhnikov@gmail.com
