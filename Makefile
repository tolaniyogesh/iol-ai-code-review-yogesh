.PHONY: help install test lint format clean run docker-build docker-run

help:
	@echo "AI Code Review Assistant - Make Commands"
	@echo "========================================"
	@echo "install       - Install dependencies"
	@echo "test          - Run tests"
	@echo "test-cov      - Run tests with coverage"
	@echo "lint          - Run linters (flake8, mypy)"
	@echo "format        - Format code with black"
	@echo "clean         - Clean up generated files"
	@echo "run           - Run locally (requires .env)"
	@echo "docker-build  - Build Docker image"
	@echo "docker-run    - Run in Docker container"

install:
	pip install -r requirements.txt

test:
	pytest -v

test-cov:
	pytest --cov=src --cov-report=html --cov-report=term

lint:
	flake8 src/ tests/
	mypy src/

format:
	black src/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache .mypy_cache htmlcov .coverage

run:
	python -m src.main

docker-build:
	docker build -t ai-code-reviewer:latest .

docker-run:
	docker run --env-file .env ai-code-reviewer:latest

docker-compose-up:
	docker-compose up

docker-compose-down:
	docker-compose down
