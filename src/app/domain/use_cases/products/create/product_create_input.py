from decimal import Decimal

from pydantic import BaseModel


class ProductCreateInput(BaseModel):
    sku: str
    name: str
    price: Decimal
    brand_id: str
