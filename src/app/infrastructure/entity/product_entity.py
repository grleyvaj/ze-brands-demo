from datetime import datetime
from decimal import Decimal

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Numeric

from app.infrastructure.db.session import Base
from app.infrastructure.entity.audit_entity import AuditMixinEntity


class ProductEntity(AuditMixinEntity, Base):
    __tablename__ = "products"

    id = Column(String(26), primary_key=True, index=True)
    sku = Column(String(64), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    brand_id = Column(String(26), ForeignKey("brands.id"), nullable=False)

    brand = relationship("BrandEntity", back_populates="products")

    def __init__(
        self,
        id: str,
        sku: str,
        name: str,
        price: Decimal,
        brand_id: str,
        created_at: datetime,
        updated_at: datetime,
    ) -> None:
        self.id = id
        self.sku = sku
        self.name = name
        self.price = price
        self.brand_id = brand_id
        self.created_at = created_at
        self.updated_at = updated_at
