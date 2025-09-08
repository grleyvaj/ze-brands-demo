from pydantic import BaseModel


class ProductUpdateEvent(BaseModel):
    product_id: str
    changes: dict
