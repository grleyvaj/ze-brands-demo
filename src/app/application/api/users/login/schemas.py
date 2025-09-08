from pydantic import BaseModel, Field


class UserLoginRequest(BaseModel):
    username: str = Field(
        ...,
        description="Username",
        example="grleyva",
    )
    password: str = Field(
        ...,
        description="User's password",
        example="MySecurePassword123!",
    )


class TokenResponse(BaseModel):
    access_token: str = Field(
        ...,
        description="Access token",
        example="wewerwerwer....",
    )
    token_type: str = "bearer"  # noqa: S105
