# scripts/run_yoyo_migrations.py
import logging
from pathlib import Path

from dotenv import load_dotenv
from yoyo import get_backend, read_migrations

from app.core.configurations import settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(env_path)


def normalize_for_yoyo(db_url: str) -> str:
    """Convert the SQLAlchemy URL to one that is valid for yoyo."""
    if db_url.startswith("postgresql+psycopg2://"):
        return db_url.replace("postgresql+psycopg2://", "postgresql://", 1)
    return db_url


def run_yoyo_migrations_sync(
    database_url: str,
    migrations_path: str = "migrations",
) -> None:
    logger.info(
        "Running yoyo migrations - db=%s migrations_path=%s",
        database_url,
        migrations_path,
    )
    backend = get_backend(database_url)  # yoyo uses psycopg2 by default
    migrations = read_migrations(migrations_path)
    with backend.lock():
        to_apply = backend.to_apply(migrations)
        if not to_apply:
            logger.info("No migrations to apply.")
            return
        logger.info("Applying %d migrations...", len(to_apply))
        backend.apply_migrations(to_apply)
        logger.info("Migrations applied.")


if __name__ == "__main__":
    raw_db_url = settings.DATABASE_URL
    raw_migration_path = settings.MIGRATION_PATH

    if not raw_db_url:
        msg = "DATABASE_URL not found in env"
        raise RuntimeError(msg)
    if not raw_migration_path:
        msg = "MIGRATION_PATH not found in env"
        raise RuntimeError(msg)

    normalized_db_url = normalize_for_yoyo(raw_db_url)
    run_yoyo_migrations_sync(normalized_db_url, raw_migration_path)
