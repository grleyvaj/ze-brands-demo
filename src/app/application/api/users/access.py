from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.application.api.users.detail.schemas import UserDetailResponse
from app.application.api.users.login.schemas import TokenResponse, UserLoginRequest
from app.application.api.users.sig_up.mappers import SigUpInputMapper
from app.application.api.users.sig_up.schemas import SigUpRequest
from app.application.containers import container
from app.domain.use_cases.users.login.login_use_case import LoginUseCase
from app.domain.use_cases.users.sig_up.sig_up_use_case import SigUpUseCase

router = APIRouter(
    prefix="",
    tags=["Access"],  # open endpoints
)


@router.post(
    "/login",
    summary="Login a user",
    description="Authenticates a user "
    "with username and password and returns a JWT access token.",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Unauthorized",
                    },
                },
            },
        },
    },
)
def login(
    request: UserLoginRequest,
    use_case: Annotated[
        LoginUseCase,
        Depends(lambda: container.resolve(LoginUseCase)),
    ],
) -> TokenResponse:
    token = use_case.login(
        username=request.username,
        password=request.password,
    )
    return TokenResponse(access_token=token)


@router.post(
    "/sigup",
    summary="Register a new user",
    description=(
        "Creates a new user account as an ANONYMOUS user of the application. "
        "Returns the user details after successful registration."
    ),
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["username", "email"],
                                "msg": "User with USERNAME 'grleyva' "
                                "or EMAIL 'grleyva.test@gmail.com' "
                                "already exists",
                                "type": "ALREADY_EXIST_USER",
                            },
                        ],
                    },
                },
            },
        },
    },
)
def sig_up(
    request: SigUpRequest,
    use_case: Annotated[
        SigUpUseCase,
        Depends(lambda: container.resolve(SigUpUseCase)),
    ],
) -> UserDetailResponse:
    user = use_case.sig_up(
        sig_up_input=SigUpInputMapper.map(request),
    )
    return UserDetailResponse(**user.model_dump())
