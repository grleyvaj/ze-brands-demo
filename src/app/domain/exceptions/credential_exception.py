from typing import Any

from app.domain.enums.code_enum import ErrorCodeEnum


class CredentialError(Exception):

    def __init__(
        self: "CredentialError",
        code: ErrorCodeEnum,
        location: list[Any],
        message: str,
    ) -> None:
        self.code = code
        self.location = location
        self.message = message
        super().__init__(self.message)
