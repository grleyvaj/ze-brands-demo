from app.domain.enums.role_enum import UserRole
from app.domain.helpers.datetime_generator import get_now_datetime
from app.domain.helpers.ulid_generator import generate_ulid
from app.domain.models.user import User
from app.domain.use_cases.users.create.user_create_input import UserCreateInput
from app.infrastructure.entity.user_entity import UserEntity


class UserMapper:

    @staticmethod
    def map_to_entity(user: UserCreateInput, role: UserRole) -> UserEntity:
        date_now = get_now_datetime()

        return UserEntity(
            id=generate_ulid(),
            username=user.username,
            email=str(user.email),
            hashed_password=user.hashed_password,
            role=role,
            created_at=date_now,
            updated_at=date_now,
        )

    @staticmethod
    def map_to_model(entity: UserEntity) -> User:
        return User(
            id=entity.id,
            username=entity.username,
            email=entity.email,
            hashed_password=entity.hashed_password,
            role=entity.role,
        )
