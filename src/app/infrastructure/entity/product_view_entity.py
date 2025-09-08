from datetime import datetime

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import BigInteger

from app.infrastructure.db.session import Base
from app.infrastructure.entity.audit_entity import AuditMixinEntity


class ProductViewCountEntity(AuditMixinEntity, Base):
    __tablename__ = "product_views"

    id = Column(String(26), primary_key=True, index=True)
    product_id = Column(String(26), ForeignKey("products.id"), nullable=False)
    view_count = Column(BigInteger, default=0)

    product = relationship("ProductEntity")

    def __init__(
        self,
        id: str,
        product_id: str,
        view_count: BigInteger,
        created_at: datetime,
        updated_at: datetime,
    ) -> None:
        self.id = id
        self.product_id = product_id
        self.view_count = view_count
        self.created_at = created_at
        self.updated_at = updated_at
