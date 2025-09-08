from fastapi import FastAPI, status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.application.handlers.detail_error_response import DetailErrorResponse
from app.application.handlers.error_response import ErrorResponse
from app.domain.exceptions.credential_exception import CredentialError
from app.domain.exceptions.data_validation_exception import DataValidationError
from app.domain.exceptions.resource_not_found_exception import ResourceNotFoundError


def _add_project_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(DataValidationError)
    async def data_validation_error(
        request: Request,
        exc: DataValidationError,
    ) -> JSONResponse:
        _ = request
        detail_error_response = DetailErrorResponse(
            detail=[
                ErrorResponse(
                    type=exc.code.value,
                    loc=exc.location,
                    msg=exc.message,
                ),
            ],
        )

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=detail_error_response.model_dump(exclude_none=True, by_alias=True),
        )

    @app.exception_handler(CredentialError)
    async def credential_error(
        request: Request,
        exc: CredentialError,
    ) -> JSONResponse:
        _ = request
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": exc.message},
        )

    @app.exception_handler(ResourceNotFoundError)
    async def not_found_error(
        request: Request,
        exc: ResourceNotFoundError,
    ) -> JSONResponse:
        _ = request
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": exc.message},
        )


def add_exception_handlers(app: FastAPI) -> None:
    return _add_project_exception_handlers(app)
