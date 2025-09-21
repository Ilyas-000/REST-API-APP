.PHONY: help build up down restart logs shell db-shell migrate makemigrations test clean backup dev-setup dev-run

help: ## Показать справку
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Собрать Docker образы
	docker compose build

up: ## Запустить все сервисы
	docker compose up -d
	@echo "API доступно по адресу: http://localhost:8000"
	@echo "Документация: http://localhost:8000/docs"

down: ## Остановить все сервисы
	docker compose down

restart: ## Перезапустить все сервисы
	docker compose restart

logs: ## Посмотреть логи
	docker compose logs -f

shell: ## Подключиться к контейнеру приложения
	docker compose exec api bash

db-shell: ## Подключиться к базе данных
	docker compose exec db psql -U user -d organizations_db

migrate: ## Выполнить миграции
	docker compose exec api alembic upgrade head

makemigrations: ## Создать новую миграцию
	@read -p "Введите описание миграции: " desc; \
	docker compose exec api alembic revision --autogenerate -m "$$desc"

test: ## Запустить тесты
	docker compose exec api python test_data.py
	docker compose exec api python api_examples.py

clean: ## Очистить Docker ресурсы
	docker compose down -v --rmi local
	docker system prune -f

backup: ## Создать резервную копию данных
	docker compose exec api python backup_restore.py backup

dev-setup: ## Настройка для разработки (без Docker)
	pip install -r requirements.txt
	@echo "Создайте базу данных PostgreSQL: organizations_db"
	@echo "Затем выполните: alembic upgrade head"

dev-run: ## Запуск для разработки (без Docker)
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

check-docker: ## Проверить статус Docker
	@docker --version && echo "✅ Docker установлен" || echo "❌ Docker не установлен"
	@docker info > /dev/null 2>&1 && echo "✅ Docker работает" || echo "❌ Docker не запущен"

status: ## Показать статус сервисов
	docker compose ps
