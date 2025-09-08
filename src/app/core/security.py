from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from app.core.configurations import settings

bearer_scheme = HTTPBearer(bearerFormat="JWT", auto_error=True)


class JWTBearer:
    """Reusable class for extracting and validating the JWT"""

    def __init__(self, auto_error: bool = True):
        self.auto_error = auto_error

    def __call__(
        self,
        credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
    ):
        if not credentials:
            if self.auto_error:
                raise HTTPException(status_code=401, detail="Missing token")
            return None
        token = credentials.credentials
        try:
            return jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )
        except jwt.JWTError as err:
            if self.auto_error:
                raise HTTPException(status_code=401, detail="Invalid token") from err
            return None
