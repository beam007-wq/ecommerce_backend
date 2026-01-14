from fastapi import HTTPException,status,Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from core.security import secret_key
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_token(token: Annotated[str,Depends(oauth2_scheme)]) -> str:
    try:
        data = jwt.decode(token,secret_key,algorithms=["HS256"])
        return data
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid token")
    
def check_admin_identify(token: Annotated[str,Depends(get_token)]):
    if token["identify"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="not permit")

def check_user_identify(token: Annotated[str,Depends(get_token)]):
    if token["identify"] != "user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="not permit")