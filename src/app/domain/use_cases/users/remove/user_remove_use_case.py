from app.domain.repositories.user_repository import UserRepository


class UserRemoveUseCase:

    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        self.user_repository = user_repository

    def remove_user(self, user_id: str) -> None:
        self.user_repository.delete_by_id(user_id)
