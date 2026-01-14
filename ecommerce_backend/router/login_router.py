from fastapi import FastAPI,HTTPException,status,Form,Depends
from typing import Annotated
from model import user
from func.sql_operation import sql_operation
from core.security import secret_key
from deps.exists import username_check_exists
import jwt

login_app = FastAPI()

@login_app.post("/login",status_code=status.HTTP_200_OK)
async def login(user: Annotated[user.User_login,Form(...)],exists = Depends(username_check_exists)) -> dict:
    if not exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="username not existed")
    
    sql = "select * from user where username = %s"
    result = sql_operation(sql,"FO",[user.username])

    if user.password != result["password"]:
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="password not correct")
            
    if result["allow_login"] != 1:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="not permit")

    payload = {"username":user.username,"identify":"user" if result["identify"] == "user" else "admin"}
    token = jwt.encode(payload,secret_key,algorithm="HS256")
    return {"access_token":token,"token_type":"bearer","redirect":"/main/user"}

@login_app.post("/registor",response_model=user.User_created)
async def registor(user: Annotated[user.User_registor,Form(...)],exists = Depends(username_check_exists)) -> user.User_created:
    if exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="username is existed")

    sql = "insert into user(username,password,identify,allow_login) values(%s,%s,%s,%s)"
    result = sql_operation(sql,"CM",(user.username,user.password,user.identify,user.allow_login))
    if result:
        return user