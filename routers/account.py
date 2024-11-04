from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models import Users
from database import SessionLocal
from sqlalchemy.orm import Session
from starlette import status
from fastapi import Depends
from typing import Annotated
from .auth import get_current_user


router=APIRouter(
    prefix='/account',
    tags=['account']
)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]


@router.get("/notifications",status_code=status.HTTP_201_CREATED)
def see_all_notifications(user=user_dependency,db=db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail="authentication failed")




