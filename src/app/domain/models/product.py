from decimal import Decimal

from pydantic import BaseModel


class Product(BaseModel):
    id: str
    sku: str
    name: str
    price: Decimal
    brand_id: str


class ProductView(BaseModel):
    id: str
    name: str
    view: int
