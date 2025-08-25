.PHONY: help install run test clean setup frontend backend all

help:
	@echo "Available commands:"
	@echo "  make setup     - Complete project setup"
	@echo "  make install   - Install dependencies"
	@echo "  make run       - Run both backend and frontend"
	@echo "  make backend   - Run backend only"
	@echo "  make frontend  - Run frontend only"
	@echo "  make test      - Run all tests"
	@echo "  make clean     - Clean cache files"

setup: install
	cd backend && python load_context.py
	@echo "Setup complete! Run 'make run' to start the application"

install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

backend:
	cd backend && uvicorn app:app --reload --host 0.0.0.0 --port 8000

frontend:
	cd frontend && npm run dev

run:
	@echo "Starting backend and frontend..."
	@make -j 2 backend frontend

test:
	cd backend && python -m pytest tests/ -v

test-quick:
	cd backend && python -m pytest tests/ -v --tb=short

test-integration:
	cd backend && python -m pytest tests/test_integration.py -v

test-challenge:
	cd backend && python -m pytest tests/test_challenge.py -v

test-api:
	cd backend && python -m pytest tests/test_api.py -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".coverage" -delete
	rm -rf .pytest_cache
	rm -rf backend/.pytest_cache
	rm -rf frontend/.next

lint:
	cd backend && python -m pylint agents.py app.py --disable=all --enable=E
	cd backend && python -m black --check .

format:
	cd backend && python -m black .

check: lint test
	@echo "All checks passed!"