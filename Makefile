.PHONY: clean build test lint format install dev-install

PROJECT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

clean:
	rm -rf $(PROJECT_DIR)/build
	rm -rf $(PROJECT_DIR)/dist
	rm -rf $(PROJECT_DIR)/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +

build: clean
	python -m build

test:
	python -m pytest

lint:
	python -m ruff check .

format:
	python -m ruff format .

install:
	pip install -e .

dev-install:
	pip install -e ".[dev]"