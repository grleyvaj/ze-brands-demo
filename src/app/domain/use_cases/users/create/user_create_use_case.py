from app.domain.enums.code_enum import ErrorCodeEnum
from app.domain.enums.role_enum import UserRole
from app.domain.exceptions.data_validation_exception import DataValidationError
from app.domain.models.user import User
from app.domain.repositories.user_repository import UserRepository
from app.domain.use_cases.users.create.user_create_input import UserCreateInput


class UserCreateUseCase:

    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        self.user_repository = user_repository

    def create_user(self, user_create_input: UserCreateInput) -> User:
        self._apply_business_validation(user_create_input)
        return self.user_repository.create(user=user_create_input, role=UserRole.ADMIN)

    def _apply_business_validation(self, create_input: UserCreateInput) -> None:
        if self.user_repository.exists_by(
            create_input.username,
            str(create_input.email),
        ):
            raise DataValidationError(
                code=ErrorCodeEnum.ALREADY_EXIST_USER,
                location=["username", "email"],
                message=f"User with USERNAME '{create_input.username}' "
                f"or EMAIL '{create_input.email}' already exists",
            )
