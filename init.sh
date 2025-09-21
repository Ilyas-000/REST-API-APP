# Ждем готовности базы данных
echo "Waiting for database..."
until PGPASSWORD=password psql -h db -U user -d organizations_db -c '\q' 2>/dev/null; do
  sleep 1
done

echo "Database is ready!"

# Выполняем миграции
alembic upgrade head

# Запускаем приложение
uvicorn app.main:app --host 0.0.0.0 --port 8000

