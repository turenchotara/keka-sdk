.PHONY: help install install-dev clean build publish test lint format check-format type-check docs serve-docs

help:
	@echo "Available commands:"
	@echo "  install      Install package in production mode"
	@echo "  install-dev  Install package in development mode with dev dependencies"
	@echo "  clean        Remove build artifacts and cache files"
	@echo "  build        Build distribution packages"
	@echo "  publish      Build and publish to PyPI"
	@echo "  test         Run tests"
	@echo "  lint         Run linting checks"
	@echo "  format       Format code with black and isort"
	@echo "  check-format Check code formatting"
	@echo "  type-check   Run type checking with mypy"
	@echo "  docs         Build documentation"
	@echo "  serve-docs   Build and serve documentation locally"

install:
	pip install .

install-dev:
	pip install -e .[dev,docs]

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

build: clean
	python -m pip install --upgrade build
	python -m build

publish: build
	python -m pip install --upgrade twine
	python -m twine upload dist/*

test:
	python -m pytest tests/ -v

lint:
	python -m flake8 keka_sdk/
	python -m mypy keka_sdk/

format:
	python -m black keka_sdk/ tests/
	python -m isort keka_sdk/ tests/

check-format:
	python -m black --check keka_sdk/ tests/
	python -m isort --check-only keka_sdk/ tests/

type-check:
	python -m mypy keka_sdk/

docs:
	cd docs && make html

serve-docs:
	cd docs && make html && python -m http.server 8000 --directory _build/html

# Development workflow
dev-setup: install-dev
	pre-commit install

dev-check: check-format lint type-check test

# CI/CD targets
ci-test: install test

ci-build: install build

.DEFAULT_GOAL := help
