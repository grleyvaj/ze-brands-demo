from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Run port configuration
    DEV_PORT: int = 8080

    # Database configuration
    DATABASE_URL: str = (
        "postgresql+psycopg2://postgres:postgres@localhost:5432/ze_brands_db"
    )

    # Migration config
    AUTO_MIGRATE: bool = False
    MIGRATION_PATH: str = "migrations"

    # Security
    SECRET_KEY: str = "supersecretkey12345"  # noqa: S105
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Default ADMIN user
    DEFAULT_ADMIN_USERNAME: str = "administrator"
    DEFAULT_ADMIN_PASSWORD: str = "Adm1n1str@tor"  # noqa: S105
    DEFAULT_ADMIN_EMAIL: str = "admin@gmail.com"

    # SES
    SES_REGION_NAME: str = "us-east-1"
    SES_SENDER_EMAIL: str = "jereztorresma@gmail.com"
    SES_RECIPIENT_EMAIL: str = "jereztorresma@gmail.com"

    # AWS
    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None
    AWS_DEFAULT_REGION: str = "us-east-1"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
