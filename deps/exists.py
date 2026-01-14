from model import user
from func.sql_operation import sql_operation

def username_check_exists(user:user.User_login | user.User_registor) -> bool:
    sql = "select 1 from user where username = %s limit 1"
    result = sql_operation(sql,"FO",[user.username])
    return True if result else False

def id_check_exists(user_id: int) -> bool:
    sql = "select 1 from user where id=%s limit 1"
    result = sql_operation(sql,"FO",[user_id])
    return True if result else False

def goods_check_exists(goods_id: int) -> bool:
    sql = "select 1 from goods where id=%s limit 1"
    result = sql_operation(sql,"FO",[goods_id])
    return True if result else False