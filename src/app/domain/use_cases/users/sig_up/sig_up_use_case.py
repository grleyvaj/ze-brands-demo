from app.domain.enums.code_enum import ErrorCodeEnum
from app.domain.enums.role_enum import UserRole
from app.domain.exceptions.data_validation_exception import DataValidationError
from app.domain.models.user import User
from app.domain.repositories.user_repository import UserRepository
from app.domain.use_cases.users.sig_up.sig_up_input import SigUpInput


class SigUpUseCase:

    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        self.user_repository = user_repository

    def sig_up(self, sig_up_input: SigUpInput) -> User:
        self._apply_business_validation_create(sig_up_input)
        return self.user_repository.create(user=sig_up_input, role=UserRole.ANONYMOUS)

    def _apply_business_validation_create(self, sig_up_input: SigUpInput) -> None:
        if self.user_repository.exists_by(
            sig_up_input.username,
            str(sig_up_input.email),
        ):
            raise DataValidationError(
                code=ErrorCodeEnum.ALREADY_EXIST_USER,
                location=["username", "email"],
                message=f"User with USERNAME '{sig_up_input.username}' "
                f"or EMAIL '{sig_up_input.email}' already exists",
            )
