from decimal import Decimal

from pydantic import BaseModel, Field


class ProductCreateRequest(BaseModel):
    brand_id: str = Field(
        ...,
        description="Brand identifier in ULID format",
        example="01K4G2APXKSSFTYR911GYBDVZX",
    )
    sku: str = Field(
        ...,
        description="Unique product code (SKU)",
        min_length=1,
        max_length=64,
        example="SKU-12345",
    )
    name: str = Field(
        ...,
        description="Product's name",
        min_length=1,
        max_length=255,
        example="T-Shirt",
    )
    price: Decimal = Field(
        ...,
        description="Product's price",
        ge=0,
        example=49.99,
    )
