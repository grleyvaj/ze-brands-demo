from pydantic import BaseModel, Field

from app.domain.enums.role_enum import UserRole


class UserDetailResponse(BaseModel):
    id: str = Field(
        ...,
        description="User identifier in ULID format",
        example="01K4EH5QV1TWJXQAJVSN4MCKM0",
    )
    email: str = Field(
        ...,
        description="Unique email address of the user",
        example="user@example.com",
    )
    username: str = Field(
        ...,
        description="Unique username of the user",
        example="user123",
    )
    hashed_password: str = Field(
        ...,
        description="Password in plain text (it will be hashed before storing)",
        example="MySecurePassword123!",
    )
    role: UserRole = Field(
        ...,
        description="Role of the user: ADMIN or ANONYMOUS",
        example="ADMIN",
    )
