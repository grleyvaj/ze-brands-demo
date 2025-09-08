from typing import Any

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    type: str = Field(
        alias="type",
        description="Error type",
        example="missing",
    )
    loc: list[Any] = Field(
        alias="loc",
        description="Error locations",
        example="['body', 'transactions']",
    )
    msg: str = Field(
        alias="msg",
        description="Error message",
        example="Field required",
    )
    input: Any | None = Field(
        alias="input",
        default=None,
        description="Input request where the error occurred",
        example="{'name': 't-shirt'}",
    )
    url: str | None = Field(
        alias="url",
        default=None,
        description="Documentation of the error for more details",
        example="https://errors.pydantic.dev/2.3/v/missing",
    )
