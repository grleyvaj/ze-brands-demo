from pydantic import BaseModel, PrivateAttr, model_validator
from pydantic.networks import EmailStr

from app.core.security_utils import hash_password


class UserCreateInput(BaseModel):
    username: str
    email: EmailStr
    password: str

    _hashed_password: str = PrivateAttr()

    @model_validator(mode="after")
    def hash_password_after_init(self):  # noqa: ANN201
        self._hashed_password = hash_password(self.password)
        return self

    @property
    def hashed_password(self) -> str:
        return self._hashed_password
