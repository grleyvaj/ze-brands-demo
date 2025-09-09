#!/usr/bin/env bash
set -euxo pipefail

# Load env file if mounted (path: /app/env/prod.env)
if [ -f /app/env/prod.env ]; then
  export $(grep -v '^#' /app/env/prod.env | xargs)
fi

# Ensure PYTHONPATH
export PYTHONPATH="/app/src:${PYTHONPATH}"

echo "[entrypoint] Waiting for Postgres to be ready (if configured)..."
# optional wait script: will exit quickly if DB not configured
if [ -f /app/scripts/wait_for_postgres.py ]; then
  poetry run python /app/scripts/wait_for_postgres.py
fi

# Run migrations (best-effort)
if [ "${AUTO_MIGRATE:-false}" = "true" ]; then
  echo "[entrypoint] Running migrations (yoyo)..."
  # run migrations but don't fail container permanently if migration command errors during a rolling deploy
  poetry run python /app/scripts/run_yoyo_migrations.py || true
fi

echo "[entrypoint] Starting uvicorn (production)"
# Exec uvicorn using poetry (ensures correct venv) and without --reload
exec poetry run uvicorn app.main:app --host 0.0.0.0 --port "${DEV_PORT:-8080}" 