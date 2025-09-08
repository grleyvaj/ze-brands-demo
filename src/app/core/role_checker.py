from fastapi import Depends, HTTPException

from app.core.security import JWTBearer


class RoleChecker:
    """Reusable class for checking roles"""

    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: dict = Depends(JWTBearer())):
        if not user or user.get("role") not in self.allowed_roles:
            raise HTTPException(status_code=401, detail="Unauthorized")
        return user
