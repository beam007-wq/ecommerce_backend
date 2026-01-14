from fastapi import FastAPI,Form,Depends,status
from typing import Annotated
from func.sql_operation import sql_operation
from model import orders
from deps.auth import check_user_identify,get_token

user_main_app = FastAPI()

@user_main_app.post("/order/create",status_code=status.HTTP_201_CREATED,dependencies=[Depends(check_user_identify)])
async def create_order(order:Annotated[orders.Order_create,Form(...)],token = Depends(get_token)) -> dict:
    sql = "insert into orders(order_NO,username,order_status,order_type,price,goods_name) values(%s,%s,%s,%s,%s,%s)"
    sql_operation(sql,"CM",(order.order_NO, token["username"], orders.Order_status.PENDING.value, order.order_type, order.price, order.goods_name))
    return {"status":"successful"}

@user_main_app.put("/order/canceled",status_code=status.HTTP_200_OK,dependencies=[Depends(check_user_identify)])
async def canceled_order(order_NO: int) -> dict:
    sql = "update orders set order_status = %s where order_NO = %s"
    sql_operation(sql,"CM",(orders.Order_status.CANCELLED.value,order_NO))
    return {"status":"successful"}

@user_main_app.put("/order/completed",dependencies=[Depends(check_user_identify)])
async def completed_order(order_NO: int):
    sql = "update orders set order_status = %s where order_NO = %s"
    sql_operation(sql,"CM",(orders.Order_status.COMPLETED.value,order_NO))
    return {"status":"successful"}

@user_main_app.post("/order/return",dependencies=[Depends(check_user_identify)])
async def return_order(order_NO: int):
    pass