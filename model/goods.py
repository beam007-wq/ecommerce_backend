from pydantic import BaseModel,Field
from decimal import Decimal

class Goods_add(BaseModel):
    name: str = Field(max_length=100)
    price: Decimal = Field(gt=0)
    description: str
    status: bool | None
    stock: int | None
    image: str = Field(max_length=255)
    tags: set[str] = []