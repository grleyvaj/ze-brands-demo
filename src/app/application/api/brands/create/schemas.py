from __future__ import annotations

from pydantic import BaseModel, Field


class BrandCreateRequest(BaseModel):
    name: str = Field(
        ...,
        description="Brand's name",
        min_length=1,
        max_length=128,
        example="Nike",
    )
    description: str | None = Field(
        None,
        description="Brand's description",
        min_length=1,
        max_length=255,
        example="Sportswear and athletic footwear",
    )
    logo_url: str | None = Field(
        None,
        description="Brand's logo URL",
        min_length=1,
        max_length=255,
        example="https://example.com/logos/nike.png",
    )
