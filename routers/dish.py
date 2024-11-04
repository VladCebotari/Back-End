from typing import Annotated


from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,HTTPException,Path
from database import SessionLocal
from starlette import status
from pydantic import BaseModel,Field

from models import Todos,Users
from .auth import get_current_user,CreateUserRequest
import base64


router=APIRouter(
    prefix='/dish',
    tags=['dish']
)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]



# def save_base64_image(base64_string):
#     with open ("image.txt","w") as f:
#         f.write(base64_string)






