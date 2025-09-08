from pydantic import BaseModel
from pydantic.networks import EmailStr

from app.domain.enums.role_enum import UserRole


class User(BaseModel):
    id: str
    username: str
    email: EmailStr
    hashed_password: str
    role: UserRole
