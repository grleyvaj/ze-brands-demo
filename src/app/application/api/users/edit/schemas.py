from pydantic import BaseModel, Field
from pydantic.networks import EmailStr


class UserUpdateRequest(BaseModel):
    email: EmailStr = Field(
        ...,
        description="Unique email address of the user",
        min_length=5,
        max_length=100,
        example="user@example.com",
    )
