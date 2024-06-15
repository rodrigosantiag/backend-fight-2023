# project settings
PROJECT_NAME  := backend-fight-2023
PROJECT_PATH  := $(shell ls */main.py | xargs dirname | head -n 1)

# venv settings
export PYTHONPATH := $(PROJECT_PATH)
export VIRTUALENV := $(PWD)/.venv
export PATH       := $(VIRTUALENV)/bin:$(PATH)

# unittest logging level
test: export LOG_LEVEL=CRITICAL

# fix make < 3.81 (macOS and old Linux distros)
ifeq ($(filter undefine,$(value .FEATURES)),)
SHELL = env PATH="$(PATH)" /bin/bash
endif

.PHONY: .env .venv

all:

.env:
	echo 'PYTHONPATH="$(PYTHONPATH)"' > .env
	cat .env_sample >> .env

.venv:
	python3.11 -m venv $(VIRTUALENV)
	pip install --upgrade pip

clean:
	rm -rf dependencies .pytest_cache .coverage
	find $(PROJECT_PATH) -name __pycache__ | xargs rm -rf
	find tests -name __pycache__ | xargs rm -rf

install-hook:
	@echo "make lint" > .git/hooks/pre-commit
	@chmod +x .git/hooks/pre-commit

install-dev: .venv .env install install-hook
	@mkdir -p test_outputs
	if [ -f requirements-dev.txt ]; then pip install -r requirements-dev.txt; fi

install:
	if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

lint:
	black --line-length=100 --target-version=py311 --check .
	flake8 --max-line-length=100 --ignore=E402,W503,E712 --exclude .venv,dependencies

format:
	black --line-length=100 --target-version=py311 .

test:
	@docker compose up --build --wait testgres
	alembic downgrade base
	alembic upgrade head
	coverage run --source=$(PROJECT_PATH) --omit=dependencies -m unittest && coverage report -m --fail-under=90
	-@docker compose down --volumes

build:
	@docker compose build

up:
	@docker compose up --build --wait api

nginx:
	@docker compose up --build --wait nginx

up-bridge:
	@docker compose -f docker-compose-bridge.yml up --build --wait api

nginx-bridge:
	@docker compose -f docker-compose-bridge.yml up --build --wait nginx

down:
	@docker compose down

logs:
	@docker compose logs -f

create-migration:
	@alembic revision -m "${description}"
