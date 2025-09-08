from pydantic import BaseModel


class Brand(BaseModel):
    id: str
    name: str
    description: str | None
    logo_url: str | None
