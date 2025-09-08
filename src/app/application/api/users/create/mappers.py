from app.application.api.users.create.schemas import UserCreateRequest
from app.domain.use_cases.users.create.user_create_input import UserCreateInput


class UserCreateInputMapper:

    @staticmethod
    def map(request: UserCreateRequest) -> UserCreateInput:
        return UserCreateInput(
            username=request.username,
            email=request.email,
            password=request.password,
        )
