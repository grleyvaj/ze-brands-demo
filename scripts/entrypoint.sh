#!/usr/bin/env bash
set -euxo pipefail

# Load .env if exists (for docker env volumes convenience)
if [ -f /app/env/local.env ]; then
  export $(grep -v '^#' /app/env/local.env | xargs)
elif [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

export PYTHONPATH="/app/src:${PYTHONPATH}"

echo "[entrypoint] Waiting for Postgres to be ready..."
poetry run python /app/scripts/wait_for_postgres.py

# Run migrations if enabled
if [ "${AUTO_MIGRATE:-false}" = "true" ]; then
  echo "[entrypoint] Running migrations (yoyo)..."
  poetry exec migrate || (echo "Migrations failed" && exit 1)
fi

echo "[entrypoint] Starting uvicorn..."
exec poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port "$DEV_PORT"