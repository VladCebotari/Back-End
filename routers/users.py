from typing import Annotated

from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,HTTPException,Path
from database import SessionLocal
from starlette import status
from pydantic import BaseModel,Field

from models import Todos,Users
from .auth import get_current_user,CreateUserRequest


router = APIRouter(
    prefix='/users',
    tags=['users']
)

class UserRequestChangePassword(BaseModel):
    password : str
    new_password : str = Field(min_length=4)

class UserRequestChangePhoneNumber(BaseModel):
    new_phone_number : str

class UserRequestChangeEmail(BaseModel):
    new_email : str

class UserRequestChangeUsername(BaseModel):
    new_username : str

class UserRequestChangeFirstname(BaseModel):
    new_firstname : str

class UserRequestChangeLastname(BaseModel):
    new_lastname : str

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')





@router.get("/get_user",status_code=status.HTTP_200_OK)
async def return_user(user: user_dependency,
                      db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail='Not authenticated')
    return db.query(Users).filter(user.get('id') == Users.id).all()


@router.put("/change_email",status_code=status.HTTP_204_NO_CONTENT)
async def update_email (   db: db_dependency,
                           user: user_dependency,
                           user_request: UserRequestChangeEmail):
    if user is None:
        raise HTTPException(status_code=401, detail='Not authenticated')
    user_model = db.query(Users).filter(user.get("id") == Users.id).first()
    user_model.email = user_request.new_email

    db.add(user_model)
    db.commit()


@router.put("/change_firstname",status_code=status.HTTP_204_NO_CONTENT)
async def update_firstname (   db: db_dependency,
                           user: user_dependency,
                           user_request: UserRequestChangeFirstname):
    if user is None:
        raise HTTPException(status_code=401, detail='Not authenticated')
    user_model = db.query(Users).filter(user.get("id") == Users.id).first()
    user_model.firstname = user_request.new_firstname

    db.add(user_model)
    db.commit()

@router.put("/change_lastname",status_code=status.HTTP_204_NO_CONTENT)
async def update_firstname (   db: db_dependency,
                           user: user_dependency,
                           user_request: UserRequestChangeLastname):
    if user is None:
        raise HTTPException(status_code=401, detail='Not authenticated')
    user_model = db.query(Users).filter(user.get("id") == Users.id).first()
    user_model.lastname = user_request.new_lastname

    db.add(user_model)
    db.commit()








# @router.put("/change_username",status_code=status.HTTP_204_NO_CONTENT)
@router.put("/change_username",status_code=status.HTTP_204_NO_CONTENT)
def update_username (db: db_dependency,
                     user: user_dependency,
                     user_request: UserRequestChangeUsername):
    if user is None:
        raise HTTPException(status_code=401, detail='Not authenticated')
    user_model = db.query(Users).filter(user.get("id") == Users.id).first()
    user_model.username = user_request.new_username

    db.add(user_model)
    db.commit()


@router.put("/change_password",status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency,
                      db: db_dependency,
                      user_request: UserRequestChangePassword):
    if user is None:
        raise HTTPException(status_code=401, detail='Not authenticated')
    user_model = db.query(Users).filter(user.get('id') == Users.id).first()

    if not bcrypt_context.verify(user_request.password,user_model.hashed_password):
        raise HTTPException(status_code=401,detail='Not authenticated')
    user_model.hashed_password = bcrypt_context.hash(user_request.new_password)

    db.add(user_model)
    db.commit()


@router.put("/update_phone_number",status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number (db: db_dependency,
                               user: user_dependency,
                               user_request: UserRequestChangePhoneNumber):
    if user is None:
        raise HTTPException(status_code=401, detail='Not authenticated')
    user_model = db.query(Users).filter(user.get("id") == Users.id).first()
    user_model.phone_number = user_request.new_phone_number

    db.add(user_model)
    db.commit()

# like
# search
# follow
# notifications