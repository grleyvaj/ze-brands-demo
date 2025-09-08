from abc import ABC, abstractmethod

from app.domain.enums.role_enum import UserRole
from app.domain.models.user import User
from app.domain.use_cases.users.create.user_create_input import UserCreateInput
from app.domain.use_cases.users.edit.user_update_input import UserUpdateInput


class UserRepository(ABC):

    @abstractmethod
    def create(
        self,
        user: UserCreateInput,
        role: UserRole,
    ) -> User:
        raise NotImplementedError

    @abstractmethod
    def find_by_username(self, username: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def exists_by(self, username: str, email: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self, user_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, user_id: str, user_update: UserUpdateInput) -> User:
        raise NotImplementedError
