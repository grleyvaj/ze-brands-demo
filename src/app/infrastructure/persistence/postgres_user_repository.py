from sqlalchemy import exists, or_, select
from sqlalchemy.exc import SQLAlchemyError

from app.core.logging_config import logger
from app.domain.enums.code_enum import ErrorCodeEnum
from app.domain.enums.role_enum import UserRole
from app.domain.exceptions.resource_not_found_exception import ResourceNotFoundError
from app.domain.models.user import User
from app.domain.repositories.user_repository import UserRepository
from app.domain.use_cases.users.create.user_create_input import UserCreateInput
from app.domain.use_cases.users.edit.user_update_input import UserUpdateInput
from app.infrastructure.db.database_repository import DatabaseRepository
from app.infrastructure.entity.user_entity import UserEntity
from app.infrastructure.persistence.mappers.user_mapper import UserMapper


class PostgresUserRepository(UserRepository):

    def __init__(self, database_repository: DatabaseRepository) -> None:
        self.database_repository = database_repository

    def create(self, user: UserCreateInput, role: UserRole) -> User:
        session = self.database_repository.get_db_session()
        try:
            user_entity = UserMapper.map_to_entity(user, role)
            session.add(user_entity)
            session.commit()
        except SQLAlchemyError:
            logger.exception("Error creating user")
            session.rollback()
            raise

        return UserMapper.map_to_model(user_entity)

    def find_by_username(self, username: str) -> User | None:
        session = self.database_repository.get_db_session()
        try:
            entity = session.scalar(
                select(UserEntity).where(UserEntity.username == username),
            )
            return UserMapper.map_to_model(entity) if entity else None
        except SQLAlchemyError:
            logger.exception(f"Error getting user with USERNAME: {username}")
            raise

    def exists_by(self, username: str, email: str) -> bool:
        session = self.database_repository.get_db_session()
        try:
            stmt = select(
                exists().where(
                    or_(UserEntity.username == username, UserEntity.email == email),
                ),
            )
            return session.scalar(stmt)
        except SQLAlchemyError:
            logger.exception(
                f"Error checking existence of user with"
                f" USERNAME: {username} or EMAIL: {email}",
            )
            raise

    def exists_by_email(self, email: str) -> bool:
        session = self.database_repository.get_db_session()
        try:
            stmt = select(exists().where(UserEntity.email == email))
            return session.scalar(stmt)
        except SQLAlchemyError:
            logger.exception(
                f"Error checking existence of user with EMAIL: {email}",
            )
            raise

    def update(self, user_id: str, user_update: UserUpdateInput) -> User:
        session = self.database_repository.get_db_session()
        try:
            stmt = select(UserEntity).where(UserEntity.id == user_id)
            user_entity = session.execute(stmt).scalar_one_or_none()

            if user_entity is None:
                raise ResourceNotFoundError(
                    code=ErrorCodeEnum.USER_NOT_FOUND,
                    location=["user_id"],
                    message=f"No user found with ID: {user_id}.",
                )

            update_data = user_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(user_entity, field, value)

            session.commit()
            session.refresh(user_entity)

            return UserMapper.map_to_model(user_entity)

        except SQLAlchemyError:
            logger.exception(f"Error updating user with ID: {user_id}")
            session.rollback()
            raise

    def delete_by_id(self, user_id: str) -> None:
        session = self.database_repository.get_db_session()
        try:
            entity = session.get(UserEntity, user_id)
            if not entity:
                return
            session.delete(entity)
            session.commit()
        except SQLAlchemyError:
            logger.exception(f"Error deleting user with ID: {user_id}")
            session.rollback()
            raise
