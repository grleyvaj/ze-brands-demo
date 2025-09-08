from pydantic import BaseModel
from pydantic.networks import EmailStr


class UserUpdateInput(BaseModel):
    email: EmailStr
