# src/app/main.py
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.application import containers  # noqa: F401
from app.application.api.brands import brands
from app.application.api.products import products
from app.application.api.users import access, users
from app.application.handlers.exception_handlers import add_exception_handlers
from app.core.configurations import settings
from app.core.logging_config import logger
from app.core.security_utils import hash_password
from app.domain.enums.role_enum import UserRole
from app.domain.helpers.datetime_generator import get_now_datetime
from app.domain.helpers.ulid_generator import generate_ulid
from app.infrastructure.db.session import Base, engine  # noqa: F401
from app.infrastructure.entity.user_entity import UserEntity
from app.openapi import openapi
from scripts.run_yoyo_migrations import normalize_for_yoyo, run_yoyo_migrations_sync


# ----------------------------
# Lifespan handler to run migrations automatically
# ----------------------------
@asynccontextmanager
async def lifespan(app: FastAPI) -> None:  # noqa: ARG001
    auto_migrate = settings.AUTO_MIGRATE
    default_admin = settings.DEFAULT_ADMIN_USERNAME
    default_email = settings.DEFAULT_ADMIN_EMAIL
    default_password = settings.DEFAULT_ADMIN_PASSWORD

    if auto_migrate:
        raw_db_url = settings.DATABASE_URL
        migrations_path = settings.MIGRATION_PATH
        normalized_db_url = normalize_for_yoyo(raw_db_url)
        logger.info("Running migrations automatically at startup...")
        await asyncio.to_thread(
            run_yoyo_migrations_sync,
            normalized_db_url,
            migrations_path,
        )
        logger.info("Migrations finished.")

    with Session(engine) as session:
        exists = session.query(UserEntity).filter_by(username=default_admin).first()
        date_now = get_now_datetime()
        if not exists:
            user = UserEntity(
                id=generate_ulid(),
                username=default_admin,
                email=default_email,
                hashed_password=hash_password(default_password),
                role=UserRole.SUPERADMIN,
                created_at=date_now,
                updated_at=date_now,
            )
            session.add(user)
            session.commit()
            logger.info("Default superadmin user created")

    yield


# ----------------------------
# FastAPI
# ----------------------------
app = FastAPI(redoc_url="/", lifespan=lifespan)

# ----------------------------
# Middleware y Exception Handlers
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
add_exception_handlers(app)

# ----------------------------
# Routers
# ----------------------------
app.include_router(access.router)
app.include_router(brands.router)
app.include_router(products.router)
app.include_router(users.router)

# ----------------------------
# OpenAPI
# ----------------------------
app.openapi_schema = openapi(app)
