/home/raquel/Descargas/README_DEPLOY.md# Helpers for local development
.PHONY: build up down logs shell migrate test lint

build:
\tdocker compose build --no-cache

up:
\tdocker compose up --build -d

down:
\tdocker compose down -v

logs:
\tdocker compose logs -f api

shell:
\tdocker compose exec api /bin/bash

migrate:
\tdocker compose exec api poetry run python scripts/run_yoyo_migrations.py

test:
\tpoetry run pytest

lint:
\tpoetry run ruff check . --fix --config ruff.toml
