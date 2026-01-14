from fastapi import FastAPI,HTTPException,Form,status,Depends,Query
from typing import Annotated
from model import goods,orders,user
from func.sql_operation import sql_operation
from deps.exists import username_check_exists,goods_check_exists,id_check_exists
from deps.auth import check_admin_identify
import json

admin_main_app = FastAPI()

#users manager 
@admin_main_app.post("/add/user",response_model=user.User_created,status_code=status.HTTP_201_CREATED,dependencies=[Depends(check_admin_identify)],tags = ["user admin"])
async def add_user(user: Annotated[user.User_registor,Form(...)],exists = Depends(username_check_exists)) -> user.User_created:
    if exists:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="username is existed")

    sql = "insert into user(username,password,identify,allow_login) values(%s,%s,%s,%s)"
    sql_operation(sql,"CM",(user.username,user.password,user.identify,user.allow_login))
    return user

@admin_main_app.delete("/delete/user",status_code=status.HTTP_200_OK,dependencies=[Depends(check_admin_identify)],tags = ["user admin"])
async def delete_user(user_id: Annotated[int,Query(...)],exists = Depends(id_check_exists)) -> dict:
    if not exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not found")
    
    sql = "delete from user where id = %s"
    sql_operation(sql,"CM",[user_id])
    return {"status":"success"}

@admin_main_app.put("/update/user",status_code=status.HTTP_200_OK,dependencies=[Depends(check_admin_identify)],tags = ["user admin"])
async def update_user(user_id: Annotated[int,Query(...)],user: Annotated[user.User_registor,Form(...)],exists = Depends(id_check_exists)):
    if not exists:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="user is not existed")
    
    sql = "update user set username=%s,password=%s,identify=%s,allow_login=%s where id=%s"
    sql_operation(sql,"CM",(user.username,user.password,user.identify,user.allow_login,user_id))
    return {"status":"success"}

@admin_main_app.get("/all/user",status_code=status.HTTP_200_OK,dependencies=[Depends(check_admin_identify)],tags = ["user admin"])
async def all_user() -> dict:
    sql = "select * from user"
    result = sql_operation(sql,"FA")
    return {"result":result}

#goods manager
@admin_main_app.post("/add/goods",status_code = status.HTTP_201_CREATED,dependencies=[Depends(check_admin_identify)],tags = ["goods admin"])
async def add_goods(goods: goods.Goods_add) -> dict:
    sql = "insert into goods(name,price,description,image,status,stock,tags) values(%s,%s,%s,%s,%s,%s,%s)"
    sql_operation(sql,"CM",(goods.name,goods.price,goods.description,goods.image,goods.status,goods.stock,json.dumps(list(goods.tags))))
    return {"status":"successful"}

@admin_main_app.put("/update/goods",status_code = status.HTTP_200_OK,dependencies=[Depends(check_admin_identify)],tags=["goods admin"])
async def update_goods(goods_id: Annotated[int,Query(...)],goods: goods.Goods_add,exists = Depends(goods_check_exists)) -> dict:
    if not exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail="not found")

    sql = "update goods set name=%s,price=%s,description=%s,status=%s,stock=%s,image=%s,tags=%s where id = %s"
    sql_operation(sql,"CM",(goods.name,goods.price,goods.description,goods.status,goods.stock,goods.image,json.dumps(list(goods.tags)),goods_id))
    return {"status":"successful"}

@admin_main_app.delete("/delete/goods",status_code = status.HTTP_200_OK,dependencies=[Depends(check_admin_identify)],tags=["goods admin"])
async def delete_goods(goods_id: Annotated[int,Query(...)],exists = Depends(goods_check_exists)) -> dict:
    if not exists:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail="not found")
    
    sql = "delete from goods where id=%s"
    sql_operation(sql,"CM",[goods_id])
    return {"status":"successful"}

@admin_main_app.get("/all/goods/enable/",status_code=status.HTTP_200_OK,dependencies=[Depends(check_admin_identify)],tags=["goods admin"])
async def enable_goods() -> dict:
    sql = "select * from goods where status=1"
    result = sql_operation(sql,"FA")
    return {"result":result}

@admin_main_app.get("/all/goods/disable/",status_code=status.HTTP_200_OK,dependencies=[Depends(check_admin_identify)],tags=["goods admin"])
async def enable_goods() -> dict:
    sql = "select * from goods where status=0"
    result = sql_operation(sql,"FA")
    return {"result":result}

#order manager 
@admin_main_app.delete("/order/delete",status_code=status.HTTP_200_OK,dependencies=[Depends(check_admin_identify)],tags=["orders admin"])
async def paid_order(order_id:int):
    sql = "delete from orders where id = %s"
    sql_operation(sql,"CM",[order_id])
    return {"status":"successful"}

@admin_main_app.put("/order/paid",status_code=status.HTTP_200_OK,dependencies=[Depends(check_admin_identify)],tags=["orders admin"])
async def paid_order():
    pass

@admin_main_app.put("/order/shipped",status_code=status.HTTP_200_OK,dependencies=[Depends(check_admin_identify)],tags=["orders admin"])
async def shipped_order(order_NO: int) -> dict:
    sql = "update orders set order_status = %s where order_NO = %s"
    sql_operation(sql,"CM",(orders.Order_status.SHIPPED.value,order_NO))
    return {"status":"successful"}