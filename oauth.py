from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from utils import verify_access_token
OAuth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token:Annotated[str,Depends(OAuth2)]):
     user_id = verify_access_token(token, HTTPException(status_code=401, detail="Could not validate credentials"))
     return user_id