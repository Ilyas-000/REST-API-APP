# REST API для справочника организаций

Это приложение реализует REST API для управления справочником организаций, зданий и видов деятельности.

## Стек технологий

- **FastAPI** - веб-фреймворк
- **SQLAlchemy** - ORM для работы с базой данных
- **Alembic** - инструмент миграций
- **PostgreSQL** - база данных
- **Pydantic** - валидация данных
- **Docker** - контейнеризация
- 
## Структура проекта

```
organization_api/
├── app/
│   ├── __init__.py
│   ├── main.py          # Основное приложение FastAPI
│   ├── models.py        # SQLAlchemy модели
│   ├── schemas.py       # Pydantic схемы
│   ├── crud.py          # CRUD операции
│   ├── database.py      # Настройка базы данных
│   ├── auth.py          # Аутентификация
│   └── dependencies.py  # Зависимости
├── alembic/             # Миграции базы данных
├── requirements.txt     # Python зависимости
├── Dockerfile          # Docker образ
├── docker-compose.yml  # Оркестрация контейнеров
├── init.sh             # Скрипт инициализации
├── test_data.py        # Скрипт для тестовых данных
└── README.md
```
