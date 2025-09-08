from pydantic import BaseModel, Field
from pydantic.networks import EmailStr


class SigUpRequest(BaseModel):
    username: str = Field(
        ...,
        description="Unique username of the user",
        min_length=3,
        max_length=50,
        example="user123",
    )
    email: EmailStr = Field(
        ...,
        description="Unique email address of the user",
        min_length=5,
        max_length=100,
        example="user@example.com",
    )
    password: str = Field(
        ...,
        description="Password in plain text (it will be hashed before storing)",
        min_length=8,
        example="MySecurePassword123!",
    )
