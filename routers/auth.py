from database import engine,get_db
from models import NoteTable,Base,UserTable
from fastapi import Depends,APIRouter,status,HTTPException
from sqlalchemy.orm import Session
from schemas import UserCreate
from utils import hash_password,verify_password,jwt_token
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)
@router.post("/register")
async def RegisterUser(user:UserCreate,db:Session=Depends(get_db),):
      email=db.query(UserTable).filter(UserTable.email==user.email).first()
      if email:
            raise HTTPException(status_code=400,detail="Bad request email Already Exist")
      hashed_pwd=hash_password(user.password)
      new_user = UserTable(email=user.email,hashed_password=hashed_pwd)
      db.add(new_user)
      db.commit()
      db.refresh(new_user)
      return new_user


@router.post("/login")
async def login(
   
    user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()], 
    db: Session = Depends(get_db)
):
    
    user = db.query(UserTable).filter(
        UserTable.email == user_credentials.username
    ).first()

    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=403, detail="Invalid Credentials")

    # Generate token...
    access_token = jwt_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
      