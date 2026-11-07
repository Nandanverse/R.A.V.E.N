# RAVEN Makefile - Common development commands

.PHONY: help setup start stop test lint typecheck migrate db-up db-down clean

# Default target
help:
	@echo "RAVEN - Risk-Aware Autonomous Vulnerability Exploration Network"
	@echo ""
	@echo "Available commands:"
	@echo "  make setup        - Run full setup (install deps, init db, etc.)"
	@echo "  make start        - Start backend and frontend"
	@echo "  make start-backend  - Start only backend"
	@echo "  make start-frontend - Start only frontend"
	@echo "  make stop         - Stop all services"
	@echo "  make test         - Run all tests"
	@echo "  make test-backend - Run backend tests"
	@echo "  make test-frontend - Run frontend tests"
	@echo "  make lint         - Run linters"
	@echo "  make typecheck    - Run type checkers"
	@echo "  make migrate      - Run database migrations"
	@echo "  make db-up        - Start database services (Docker)"
	@echo "  make db-down      - Stop database services"
	@echo "  make clean        - Clean build artifacts"

# Setup
setup:
	@./setup.sh

setup-windows:
	@powershell -ExecutionPolicy Bypass -File setup.ps1

# Start services
start:
	@./start.sh

start-backend:
	@cd backend && .venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

start-frontend:
	@cd frontend && npm run dev

# Stop services
stop:
	@pkill -f "uvicorn app.main:app" || true
	@pkill -f "vite" || true
	@echo "Services stopped"

# Testing
test: test-backend test-frontend

test-backend:
	@cd backend && .venv/bin/python -m pytest -v

test-frontend:
	@cd frontend && npm run test

test-e2e:
	@cd frontend && npm run test:e2e

# Linting
lint: lint-backend lint-frontend

lint-backend:
	@cd backend && .venv/bin/ruff check .
	@cd backend && .venv/bin/mypy --strict app

lint-frontend:
	@cd frontend && npm run lint

# Type checking
typecheck: typecheck-backend typecheck-frontend

typecheck-backend:
	@cd backend && .venv/bin/mypy --strict app

typecheck-frontend:
	@cd frontend && npm run typecheck

# Database
migrate:
	@cd backend && .venv/bin/alembic upgrade head

migrate-create:
	@cd backend && .venv/bin/alembic revision --autogenerate -m "$(MSG)"

db-up:
	@docker compose up -d postgres redis

db-down:
	@docker compose down

db-logs:
	@docker compose logs -f postgres redis

# Clean
clean:
	@rm -rf backend/.venv
	@rm -rf frontend/node_modules
	@rm -rf frontend/dist
	@rm -rf backend/__pycache__
	@rm -rf backend/.pytest_cache
	@rm -rf backend/.mypy_cache
	@rm -rf backend/.ruff_cache
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "Cleaned build artifacts"

# Development helpers
shell-backend:
	@cd backend && .venv/bin/python

shell-frontend:
	@cd frontend && npx ts-node

logs-backend:
	@tail -f backend/logs/app.log 2>/dev/null || echo "No log file found"

# Docker
docker-build:
	@docker compose build

docker-up:
	@docker compose up -d

docker-down:
	@docker compose down

docker-logs:
	@docker compose logs -f