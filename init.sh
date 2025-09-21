set -e

echo "🚀 Инициализация приложения..."

# Функция ожидания готовности БД
wait_for_db() {
    echo "⏳ Ожидание готовности PostgreSQL..."
    until pg_isready -h db -p 5432 -U user; do
        echo "PostgreSQL недоступен - ожидаем..."
        sleep 2
    done
    echo "✅ PostgreSQL готов!"
}

# Функция проверки подключения к БД
test_db_connection() {
    echo "🔍 Проверка подключения к базе данных..."
    python -c "
from app.database import engine
from sqlalchemy import text
try:
    with engine.connect() as conn:
        result = conn.execute(text('SELECT 1')).scalar()
    print('✅ Подключение к БД успешно')
except Exception as e:
    print(f'❌ Ошибка подключения: {e}')
    exit(1)
"
}

# Основной процесс инициализации
main() {
    wait_for_db
    test_db_connection
    
    echo "📦 Применение миграций..."
    alembic upgrade head
    
    echo "🎯 Запуск приложения..."
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
}

# Запуск с обработкой ошибок
if ! main; then
    echo "❌ Ошибка при инициализации приложения"
    exit 1
fi