from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt, JWTError


router=APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY='cheia_secreta'
ALGORITHM='HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_bearer=OAuth2PasswordBearer(tokenUrl='auth/token')

class CreateUserRequest(BaseModel):
    email:str
    username:str
    firstname:str
    lastname:str
    password:str
    role:str
    phone_number:str


class Token(BaseModel):
    access_token:str
    token_type:str



def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session,Depends(get_db)]

def authenticate_user(username: str,password: str,db):
    user=db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.hashed_password):
        return False
    return user


def create_access_token(username: str,user_id: int,role: str,expires_delta: timedelta):

    encode={'sub': username,'id': user_id,'role': role}
    # expires=datetime.utcnow() + expires_delta
    expires = datetime.now() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode,SECRET_KEY,ALGORITHM)

# datetime.datime.now(datetime.UTC)


async def get_current_user(token :Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role : str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
        return {'username': username,'id': user_id,'user_role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user')




@router.post("/signup",status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    existing_user=db.query(Users).filter(
        (Users.username == create_user_request.username) |
        (Users.email == create_user_request.email )
    ).first()


    if existing_user:
        if existing_user.username == create_user_request.username:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
        if existing_user.email == create_user_request.email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")


    create_user_model = Users (
        email = create_user_request.email,
        username = create_user_request.username,
        firstname=create_user_request.firstname,
        lastname = create_user_request.lastname,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        role = create_user_request.role,
        is_active=True,
        phone_number=create_user_request.phone_number
    )
    db.add(create_user_model)
    db.commit()


@router.post("/token",response_model=Token)
async def login_for_access_token (form_data : Annotated[OAuth2PasswordRequestForm,Depends()],
                                  db:db_dependency):
    user=authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user')

    token=create_access_token(user.username,user.id,user.role,timedelta(minutes=150))
    return {'access_token':token,'token_type': 'bearer'}

