from datetime import datetime

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.infrastructure.db.session import Base
from app.infrastructure.entity.audit_entity import AuditMixinEntity


class BrandEntity(AuditMixinEntity, Base):
    __tablename__ = "brands"

    id = Column(String(26), primary_key=True, index=True)
    name = Column(String(128), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)
    logo_url = Column(String(255), nullable=True)

    products = relationship("ProductEntity", back_populates="brand")

    def __init__(
        self,
        id: str,
        name: str,
        description: str | None,
        logo_url: str | None,
        created_at: datetime,
        updated_at: datetime,
    ) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.logo_url = logo_url
        self.created_at = created_at
        self.updated_at = updated_at
