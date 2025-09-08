from decimal import Decimal

from pydantic import BaseModel, Field


class ProductDetailResponse(BaseModel):
    id: str = Field(
        ...,
        description="Product identifier in ULID format",
        example="01K4EH5T4YQERHJ99RM1SWYV99",
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
    brand_id: str = Field(
        ...,
        description="Brand identifier in ULID format",
        example="01K4G2APXKSSFTYR911GYBDVZX",
    )
