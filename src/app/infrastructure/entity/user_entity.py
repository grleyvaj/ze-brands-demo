from datetime import datetime

from sqlalchemy import Column, String
from sqlalchemy.sql.sqltypes import Enum

from app.domain.enums.role_enum import UserRole
from app.infrastructure.db.session import Base
from app.infrastructure.entity.audit_entity import AuditMixinEntity


class UserEntity(AuditMixinEntity, Base):
    __tablename__ = "users"

    id = Column(String(26), primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(
        Enum(UserRole, name="user_role"),
        nullable=False,
        default=UserRole.ANONYMOUS,
    )

    def __init__(
        self,
        id: str,
        username: str,
        email: str,
        hashed_password: str,
        role: UserRole,
        created_at: datetime,
        updated_at: datetime,
    ) -> None:
        self.id = id
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
        self.role = role
        self.created_at = created_at
        self.updated_at = updated_at
