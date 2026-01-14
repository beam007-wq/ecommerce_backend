from enum import IntEnum
from pydantic import BaseModel,Field
from decimal import Decimal

class Order_status(IntEnum):
    PENDING = 0 # 待支付
    PAID = 1 
    SHIPPED = 2
    COMPLETED = 3
    CANCELLED = 4
    RETURNED = 5

class Order_type(IntEnum):
    NORMAL = 0 # 普通订单 
    PRE_SALE = 1 # 预售
    GROUP_BUY = 2 # 拼团
    FLASH_SALE = 3 # 秒杀

class Order_create(BaseModel):
    order_NO: int = Field(gt=0)
    order_type: Order_type = Field(description="0普通 1预售 2拼团 3秒杀")
    price: Decimal
    goods_name: str = Field(max_length=200)