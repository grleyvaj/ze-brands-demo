from app.domain.enums.code_enum import ErrorCodeEnum
from app.domain.exceptions.data_validation_exception import DataValidationError
from app.domain.models.user import User
from app.domain.repositories.user_repository import UserRepository
from app.domain.use_cases.users.edit.user_update_input import UserUpdateInput


class UserUpdateUseCase:

    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        self.user_repository = user_repository

    def update_user(self, user_id: str, update_input: UserUpdateInput) -> User:
        self._apply_business_validation(update_input)
        return self.user_repository.update(user_id=user_id, user_update=update_input)

    def _apply_business_validation(self, update_input: UserUpdateInput) -> None:
        if self.user_repository.exists_by_email(str(update_input.email)):
            raise DataValidationError(
                code=ErrorCodeEnum.ALREADY_EXIST_USER,
                location=["username", "email"],
                message=f"User with EMAIL '{update_input.email}' already exists",
            )
