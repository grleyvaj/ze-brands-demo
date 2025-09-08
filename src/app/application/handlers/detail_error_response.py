from pydantic import BaseModel, Field

from app.application.handlers.error_response import ErrorResponse


class DetailErrorResponse(BaseModel):
    detail: list[ErrorResponse] = Field(
        alias="detail",
        description="Detail of Errors",
    )
