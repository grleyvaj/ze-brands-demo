from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from app.application.api.users.create.mappers import UserCreateInputMapper
from app.application.api.users.create.schemas import UserCreateRequest
from app.application.api.users.detail.schemas import UserDetailResponse
from app.application.api.users.edit.schemas import UserUpdateRequest
from app.application.containers import container
from app.core.role_checker import RoleChecker
from app.domain.use_cases.users.create.user_create_use_case import UserCreateUseCase
from app.domain.use_cases.users.edit.user_update_input import UserUpdateInput
from app.domain.use_cases.users.edit.user_update_use_case import UserUpdateUseCase
from app.domain.use_cases.users.remove.user_remove_use_case import UserRemoveUseCase

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "",
    dependencies=[Depends(RoleChecker(["SUPERADMIN", "ADMIN"]))],
    summary="Create a new admin user",
    description=(
        "Creates a new user with ADMIN role. "
        " Only users with ADMIN permissions can perform this action. "
        "Returns the details of the newly created admin user."
    ),
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["username", "email"],
                                "msg": "Username already exists",
                                "type": "ALREADY_EXIST_USER",
                            },
                        ],
                    },
                },
            },
        },
        status.HTTP_403_FORBIDDEN: {
            "content": {
                "application/json": {
                    "example": {
                        "detail": "You do not have permission to perform this action",
                    },
                },
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "content": {
                "application/json": {
                    "example": {"detail": "Product not found"},
                },
            },
        },
    },
)
def create_user(
    request: UserCreateRequest,
    use_case: Annotated[
        UserCreateUseCase,
        Depends(lambda: container.resolve(UserCreateUseCase)),
    ],
) -> UserDetailResponse:
    user = use_case.create_user(
        user_create_input=UserCreateInputMapper.map(request),
    )
    return UserDetailResponse(**user.model_dump())


@router.put(
    "/{user_id}",
    dependencies=[Depends(RoleChecker(["ADMIN"]))],
    summary="Update user's email",
    description="Updates the email of an existing user. "
    "Only admins can perform this action.",
    responses={
        status.HTTP_403_FORBIDDEN: {
            "content": {
                "application/json": {
                    "example": {
                        "detail": "You do not have permission to perform this action",
                    },
                },
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "content": {
                "application/json": {"example": {"detail": "User not found"}},
            },
        },
    },
)
def update_user(
    use_case: Annotated[
        UserUpdateUseCase,
        Depends(lambda: container.resolve(UserUpdateUseCase)),
    ],
    request: UserUpdateRequest,
    user_id: Annotated[
        str,
        Path(
            ...,
            description="User identifier in ULID format",
            examples=["01K4EH5T4YQERHJ99RM1SWYV99"],
        ),
    ],
) -> UserDetailResponse:
    updated_user = use_case.update_user(
        user_id=user_id,
        update_input=UserUpdateInput(**request.model_dump()),
    )
    return UserDetailResponse(**updated_user.model_dump())


@router.delete(
    "/{user_id}",
    dependencies=[Depends(RoleChecker(["ADMIN"]))],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user",
    description="Deletes a user by ID. Only admins can perform this action.",
    responses={
        status.HTTP_403_FORBIDDEN: {
            "content": {
                "application/json": {
                    "example": {
                        "detail": "You do not have permission to perform this action",
                    },
                },
            },
        },
    },
)
def delete_user(
    use_case: Annotated[
        UserRemoveUseCase,
        Depends(lambda: container.resolve(UserRemoveUseCase)),
    ],
    user_id: Annotated[
        str,
        Path(
            ...,
            description="User identifier in ULID format",
            examples=["01K4EH5T4YQERHJ99RM1SWYV99"],
        ),
    ],
) -> None:
    use_case.remove_user(user_id)
