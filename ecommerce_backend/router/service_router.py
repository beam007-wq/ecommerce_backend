from fastapi import FastAPI,Depends,status,Query
from typing import Annotated
from func.sql_operation import sql_operation
from deps.auth import get_token
import json

service = FastAPI()
@service.get("/all/goods",status_code = status.HTTP_200_OK,tags=["goods user and admin"])
async def all_goods(token = Depends(get_token)) -> dict:
    sql = "select * from goods" if token["identify"] == "admin" else "select name,price,image,tags from goods"
    result = sql_operation(sql,"FA")
    return {"result":result}

@service.get("/all/goods/tag_filter/",status_code=status.HTTP_200_OK,tags=["goods user and admin"])
async def filter_goods(tags: Annotated[set[str],Query(...)],token = Depends(get_token)) -> dict:
    #JSON_CONTAIN 精准匹配
    sql = "select * from goods where JSON_OVERLAPS(tags,%s)" if token["identify"] == "admin" else "select name,price,image,tags from goods where JSON_CONTAINS(tags,%s)"
    result = sql_operation(sql,"FA",[json.dumps(list(tags))])
    return {"result":result}

@service.get("/all/orders/",status_code=status.HTTP_200_OK,tags=["orders user and admin"])
async def all_order(token = Depends(get_token)) -> dict:
    sql = "select * from orders where username=%s" if token["identify"] == "user" else "select * from orders"
    result = sql_operation(sql,"FA",[token["username"]]) if token["identify"] == "user" else sql_operation(sql,"FA")
    return {"result":result}