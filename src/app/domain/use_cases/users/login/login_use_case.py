from datetime import UTC, datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from app.core.configurations import settings
from app.domain.enums.code_enum import ErrorCodeEnum
from app.domain.exceptions.credential_exception import CredentialError
from app.domain.repositories.user_repository import UserRepository

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__ident="2b",
)


class LoginUseCase:

    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def login(self, username: str, password: str) -> str:
        user = self.user_repository.find_by_username(username)
        if not user or not self._verify_password(password, user.hashed_password):
            raise CredentialError(
                code=ErrorCodeEnum.INVALID_CREDENTIALS,
                location=["username", "password"],
                message="Invalid credentials",
            )
        return self._create_access_token({"sub": user.id, "role": user.role.value})

    @staticmethod
    def _verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def _create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        expire = datetime.now(UTC) + (
            expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        to_encode.update({"exp": expire})
        if not settings.SECRET_KEY:
            msg = "SECRET_KEY is not set"
            raise RuntimeError(msg)
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
