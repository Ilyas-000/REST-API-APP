# 🏢 REST API для справочника организаций

## 📁 Структура проекта

```
organization_api/
├── app/                          # Основной код приложения
│   ├── __init__.py                  # Маркер Python пакета
│   ├── main.py                      # FastAPI приложение и роуты
│   ├── models.py                    # SQLAlchemy модели
│   ├── schemas.py                   # Pydantic схемы
│   ├── crud.py                      # CRUD операции
│   ├── database.py                  # Настройка БД
│   ├── auth.py                      # Авторизация
│   └── dependencies.py              # FastAPI зависимости
├── alembic/                      # Миграции базы данных
│   ├── versions/                 # Файлы миграций
│   │   └── 20241201_1200_001_initial_migration.py
│   ├── env.py                       # Настройка Alembic
│   └── script.py.mako              # Шаблон для миграций
├── alembic.ini                      # Конфигурация Alembic
├── requirements.txt                 # Python зависимости  
├── Dockerfile                       # Docker образ
├── docker-compose.yml               # Оркестрация контейнеров
├── init.sh                          # Скрипт инициализации
├── .dockerignore                    # Исключения для Docker
├── .gitignore                       # Исключения для Git
├── .env                             # Переменные окружения (создать)
├── Makefile                         # Команды для разработки
├── README.md                     # Документация проекта
└── Тестирование и утилиты:
    ├── test_data.py                 # Заполнение тестовыми данными
    ├── api_examples.py              # Примеры использования API
    ├── stress_test.py               # Нагрузочное тестирование
    ├── monitoring.py                # Мониторинг здоровья API
    └── backup_restore.py            # Резервное копирование
```

## 🚀 Быстрый запуск

### Вариант 1: С Docker (рекомендуется)

1. **Создать файл `.env`:**
```bash
DATABASE_URL=postgresql://user:password@db:5432/organizations_db
API_KEY=your-secret-api-key-here
```

2. **Запустите проект:**
```bash
# Собрать и запустить
make up
# или
docker-compose up --build

# Заполнить тестовыми данными
python test_data.py

# Протестировать API
python api_examples.py
```

3. **Доступ к приложению:**
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Вариант 2: Локальная разработка

```bash
# Установка зависимостей
pip install -r requirements.txt

# Настройка БД (PostgreSQL должен быть установлен)
createdb organizations_db

# Миграции
alembic upgrade head

# Заполнение данными
python test_data.py

# Запуск сервера
uvicorn app.main:app --reload
```

## API Документация

### Авторизация
Все запросы требуют заголовок:
```
Authorization: Bearer your-secret-api-key-here
```

### Основные эндпоинты

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| `GET` | `/organizations/by-building/{building_id}` | Организации в здании |
| `GET` | `/organizations/by-activity/{activity_id}` | Организации по деятельности |
| `GET` | `/organizations/in-radius` | Поиск в радиусе |
| `GET` | `/organizations/in-rectangle` | Поиск в области |
| `GET` | `/organizations/{organization_id}` | Информация об организации |
| `GET` | `/organizations/search/by-name` | Поиск по названию |
| `GET` | `/buildings` | Список зданий |
| `POST` | `/organizations` | Создать организацию |
| `POST` | `/buildings` | Создать здание |
| `POST` | `/activities` | Создать вид деятельности |


### Особенности реализации

- **Иерархический поиск** - поиск по "Еда" включает все дочерние виды
- **Географический поиск** - точный расчет расстояний (формула Haversine)
- **Оптимизация запросов** - `joinedload` против N+1 проблемы
- **Валидация данных** - строгая типизация через Pydantic
- **Безопасность** - защита от SQL инъекций, валидация координат


### Переменные окружения
Создайте файл `.env`:
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/organizations_db
API_KEY=your-secret-api-key-here
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=organizations_db
```

### Environment Variables
```bash
# Production .env
DATABASE_URL=postgresql://prod_user:secure_password@prod_db:5432/organizations_prod
API_KEY=super-secure-production-api-key-here
POSTGRES_USER=prod_user
POSTGRES_PASSWORD=secure_password
POSTGRES_DB=organizations_prod
```

### Тестовые данные
Скрипт `test_data.py` создает:
- 4 здания в разных городах
- Иерархию видов деятельности (3 уровня)
- 5 организаций с различными характеристиками

### API клиенты
```python
# Python клиент
import requests

class OrganizationsAPI:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"}
    
    def search_by_name(self, name):
        response = requests.get(
            f"{self.base_url}/organizations/search/by-name",
            params={"name": name},
            headers=self.headers
        )
        return response.json()

# Использование
api = OrganizationsAPI("http://localhost:8000", "your-api-key")
results = api.search_by_name("Рога")
```
