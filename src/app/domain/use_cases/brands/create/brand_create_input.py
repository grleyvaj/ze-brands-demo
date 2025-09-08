from pydantic import BaseModel


class BrandCreateInput(BaseModel):
    name: str
    description: str | None
    logo_url: str | None
