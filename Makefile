.PHONY: up down logs migrate seed test lint fmt openapi erd api-client

up:          ## start everything
	@test -f .env || cp .env.example .env
	docker compose up --build -d
	@echo "API http://localhost:8000/docs  ·  Frontend http://localhost:3000"
down:
	docker compose down
logs:
	docker compose logs -f api worker
migrate:     ## apply database migrations
	docker compose exec api alembic upgrade head
seed:        ## load demo org, users and tender
	docker compose exec api python -m scripts.seed
test:
	docker compose exec api pytest
lint:
	docker compose exec api sh -c "ruff check . && ruff format --check . && mypy"
fmt:
	docker compose exec api sh -c "ruff check --fix . && ruff format ."
openapi:     ## regenerate docs/openapi.json and the frontend client
	docker compose exec api python -m scripts.export_openapi
	cd frontend && npm run gen:api
erd:
	docker compose exec api python -m scripts.export_erd
