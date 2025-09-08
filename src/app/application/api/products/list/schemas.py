from pydantic import BaseModel, Field


class ProductListItemResponse(BaseModel):
    id: str = Field(
        ...,
        description="Product identifier in ULID format",
        example="01K4EH5T4YQERHJ99RM1SWYV99",
    )
    name: str = Field(
        ...,
        description="Product's name",
        example="T-Shirt",
    )
    views: int = Field(
        ...,
        description="Product's views",
        example=5,
    )


class ProductListResponse(BaseModel):
    products: list[ProductListItemResponse] = Field(
        ...,
        description="Product list with its views",
    )
