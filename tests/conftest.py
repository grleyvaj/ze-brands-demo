# tests/conftest.py
import importlib
import logging
import os
import pathlib
from collections.abc import Generator
from datetime import UTC, datetime, timedelta
from typing import Any

import psycopg2
import pytest
from fastapi.testclient import TestClient
from jose import jwt
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine, text
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.pool import NullPool
from sqlalchemy.sql.functions import func

import app.infrastructure.db.database_repository as repo_mod
import app.infrastructure.db.session as db_session_mod
from app.core.configurations import settings
from app.domain.repositories.brand_repository import BrandRepository
from app.domain.repositories.product_repository import ProductRepository
from app.domain.repositories.product_view_repository import ProductViewRepository
from app.domain.repositories.user_repository import UserRepository
from app.domain.use_cases.brands.create.brand_create_use_case import BrandCreateUseCase
from app.domain.use_cases.products.create.product_create_use_case import (
    ProductCreateUseCase,
)
from app.domain.use_cases.products.view_report.product_view_report_use_case import (
    ProductViewReportUseCase,
)
from app.domain.use_cases.users.create.user_create_use_case import UserCreateUseCase
from app.infrastructure.db.database_repository import DatabaseRepository
from app.infrastructure.db.session import Base
from app.infrastructure.persistence.postgres_brand_repository import (
    PostgresBrandRepository,
)
from app.infrastructure.persistence.postgres_product_repository import (
    PostgresProductRepository,
)
from app.infrastructure.persistence.postgres_product_view_repository import (
    PostgresProductViewRepository,
)
from app.infrastructure.persistence.postgres_user_repository import (
    PostgresUserRepository,
)
from app.main import app

# Default env for test
os.environ.setdefault("SECRET_KEY", "supersecretkey12345")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("TEST_DEBUG", "true")

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")
logger = logging.getLogger("tests.conftest")


# -------------------------
#  FIXTURES
# -------------------------
@pytest.fixture(scope="session", autouse=True)
def recreate_db_and_load_fixtures(
    postgresql_proc: Any,
):
    """
    - Drop/create the test DB on the pytest-postgresql server.
    - Set settings.DATABASE_URL and os.environ["DATABASE_URL"].
    - Create tables and load SQL fixtures.
    - Reconfigure app.infrastructure.db.session to use TEST engine (NullPool).
    """
    user = postgresql_proc.user
    password = postgresql_proc.password
    host = postgresql_proc.host
    port = postgresql_proc.port
    dbname = postgresql_proc.dbname  # e.g. "test_db" or "ze_brands_test"

    # 1) connect to admin DB and DROP/CREATE the database
    admin_conn = psycopg2.connect(
        dbname="postgres",
        user=user,
        password=password,
        host=host,
        port=port,
    )
    admin_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = admin_conn.cursor()

    cur.execute(
        """
        SELECT pg_terminate_backend(pid)
        FROM pg_stat_activity
        WHERE datname = %s AND pid <> pg_backend_pid();
        """,
        (dbname,),
    )
    cur.fetchall()

    try:
        cur.execute(
            sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(dbname)),
        )
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))
    finally:
        try:
            cur.close()
        except Exception:
            pass
        try:
            admin_conn.close()
        except Exception:
            pass

    # 2) form DSN and set settings + env
    creds = f"{user}:{password}" if password else f"{user}"
    test_database_url = f"postgresql+psycopg2://{creds}@{host}:{port}/{dbname}"

    try:
        settings.DATABASE_URL = test_database_url
    except Exception:
        pass
    os.environ["DATABASE_URL"] = test_database_url

    # 3) create tables and load SQL fixtures using NullPool to avoid pool finalizer errors
    engine = create_engine(test_database_url, future=True, poolclass=NullPool)
    try:
        Base.metadata.create_all(bind=engine)

        with engine.begin() as conn:
            sql_dir = pathlib.Path("tests/assets/tables")
            if sql_dir.exists():
                for sql_file in sorted(sql_dir.glob("*.sql")):
                    txt = sql_file.read_text(encoding="utf-8")
                    if txt.strip():
                        # execute SQL file content
                        conn.execute(text(txt))

            # diagnostics
            try:
                conn.execute(text("select current_database();")).scalar_one()
                conn.execute(text("select current_schema();")).scalar_one()
            except Exception:
                pass

            try:
                tables = list(Base.metadata.sorted_tables)

                for t in tables:
                    conn.execute(select(func.count()).select_from(t)).scalar_one()
            except Exception:
                pass
    finally:
        try:
            engine.dispose()
        except Exception:
            pass

    # 4) reconfigure app.infrastructure.db.session so the app uses TEST engine (NullPool)
    if getattr(db_session_mod, "engine", None) is not None:
        db_session_mod.engine.dispose()

    new_engine = create_engine(test_database_url, future=True, poolclass=NullPool)
    new_session_local = sessionmaker(bind=new_engine, autoflush=False, autocommit=False)

    db_session_mod.engine = new_engine
    db_session_mod.SessionLocal = new_session_local

    importlib.reload(repo_mod)

    return test_database_url


@pytest.fixture(autouse=True)
def db_session(recreate_db_and_load_fixtures: str) -> Generator[Session, None, None]:
    """
    Provide a SQLAlchemy session for tests. Uses NullPool engines to avoid
    pool finalizer tracebacks when the server closes connections.
    """
    test_database_url = recreate_db_and_load_fixtures
    engine = create_engine(test_database_url, future=True, poolclass=NullPool)
    testing_session_local = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    db = testing_session_local()
    try:
        yield db
    finally:
        try:
            db.close()
        except Exception:
            pass
        try:
            engine.dispose()
        except Exception:
            pass


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """
    Import app here so it uses patched settings and session; override dependency to use test session.
    """

    repo = DatabaseRepository()
    repo._session = db_session

    try:
        app.dependency_overrides[DatabaseRepository.get_db_session] = lambda: db_session
    except Exception:
        pass

    client = TestClient(app)
    yield client

    try:
        app.dependency_overrides.pop(DatabaseRepository.get_db_session, None)
    except Exception:
        pass


@pytest.fixture
def test_token() -> str:
    payload = {
        "sub": "01K4H2DVXW24B09C20NZWMB50T",
        "role": "ADMIN",
        "exp": datetime.now(UTC) + timedelta(minutes=60),
    }
    return jwt.encode(
        payload,
        os.environ.get("SECRET_KEY", "supersecretkey12345"),
        algorithm=os.environ.get("ALGORITHM", "HS256"),
    )


@pytest.fixture
def container_test(db_session: Session) -> Generator[dict[type, object], None, None]:
    test_db_repo = DatabaseRepository()
    test_db_repo._session = db_session

    user_repo = PostgresUserRepository(database_repository=test_db_repo)
    brand_repo = PostgresBrandRepository(database_repository=test_db_repo)
    product_repo = PostgresProductRepository(database_repository=test_db_repo)
    view_repo = PostgresProductViewRepository(database_repository=test_db_repo)

    container = {}
    container[UserRepository] = user_repo
    container[BrandRepository] = brand_repo
    container[ProductRepository] = product_repo
    container[ProductViewRepository] = view_repo

    container[UserCreateUseCase] = UserCreateUseCase(user_repository=user_repo)
    container[BrandCreateUseCase] = BrandCreateUseCase(brand_repository=brand_repo)
    container[ProductCreateUseCase] = ProductCreateUseCase(
        product_repository=product_repo,
        brand_repository=brand_repo,
    )
    container[ProductViewReportUseCase] = ProductViewReportUseCase(
        product_repository=product_repo,
    )

    yield container

    db_session.rollback()
