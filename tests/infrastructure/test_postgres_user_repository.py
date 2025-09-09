import pytest
import ulid

from app.domain.enums.role_enum import UserRole
from app.domain.exceptions.resource_not_found_exception import ResourceNotFoundError
from app.domain.repositories.user_repository import UserRepository
from app.domain.use_cases.users.create.user_create_input import UserCreateInput
from app.domain.use_cases.users.edit.user_update_input import UserUpdateInput
from app.infrastructure.persistence.postgres_user_repository import (
    PostgresUserRepository,
)


class TestPostgresUserRepository:

    def test_create_and_find_user(self, container_test: dict) -> None:
        repo: PostgresUserRepository = container_test[UserRepository]

        ulid_str = ulid.new().str
        input_data = UserCreateInput(
            username=f"user_{ulid_str}",
            email=f"user{ulid_str}@example.com",
            password="StrongPass123",
        )

        user = repo.create(input_data, UserRole.ADMIN)

        assert user.id is not None
        assert user.username == f"user_{ulid_str}"
        assert user.email == f"user{ulid_str}@example.com"
        assert user.hashed_password != "StrongPass123"
        assert user.role == UserRole.ADMIN

        found = repo.find_by_username(f"user_{ulid_str}")
        assert found is not None
        assert found.id == user.id

    def test_find_by_username_returns_none_if_not_found(
        self,
        container_test: dict,
    ) -> None:
        repo: PostgresUserRepository = container_test[UserRepository]

        result = repo.find_by_username("nonexistent_user")
        assert result is None

    def test_exists_by_and_exists_by_email(self, container_test: dict) -> None:
        repo: PostgresUserRepository = container_test[UserRepository]

        ulid_str = ulid.new().str
        input_data = UserCreateInput(
            username=f"user_{ulid_str}",
            email=f"user{ulid_str}@example.com",
            password="StrongPass123",
        )
        user = repo.create(input_data, UserRole.ADMIN)

        assert repo.exists_by(username=user.username, email="other@example.com") is True
        assert repo.exists_by(username="otheruser", email=user.email) is True
        assert repo.exists_by(username="nouser", email="noemail@example.com") is False

        assert repo.exists_by_email(user.email) is True
        assert repo.exists_by_email("unknown@example.com") is False

    def test_update_user_success(self, container_test: dict) -> None:
        repo: PostgresUserRepository = container_test[UserRepository]

        ulid_str = ulid.new().str
        user = repo.create(
            UserCreateInput(
                username=f"user_{ulid_str}",
                email=f"user{ulid_str}@example.com",
                password="Secret123",
            ),
            UserRole.ANONYMOUS,
        )

        updated = repo.update(
            user.id,
            UserUpdateInput(email=f"updated{ulid_str}@example.com"),
        )
        assert updated.email == f"updated{ulid_str}@example.com"

    def test_update_user_not_found_raises(self, container_test: dict) -> None:
        repo: PostgresUserRepository = container_test[UserRepository]

        with pytest.raises(ResourceNotFoundError):
            repo.update(
                "01K4INVALIDUSERID",
                UserUpdateInput(email="doesnotexist@example.com"),
            )

    def test_delete_user(self, container_test: dict) -> None:
        repo: PostgresUserRepository = container_test[UserRepository]

        ulid_str = ulid.new().str
        user = repo.create(
            UserCreateInput(
                username=f"user_{ulid_str}",
                email=f"user{ulid_str}@example.com",
                password="Secret123",
            ),
            UserRole.ANONYMOUS,
        )

        repo.delete_by_id(user.id)

        found = repo.find_by_username(user.username)
        assert found is None

    def test_delete_user_non_existent_does_not_fail(self, container_test: dict) -> None:
        repo: PostgresUserRepository = container_test[UserRepository]

        repo.delete_by_id("01K4NONEXISTENTUSER")
