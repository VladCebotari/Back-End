from typing import Annotated

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session
from fastapi import APIRouter,HTTPException,Form,Query
# from starlette.responses import JSONResponse

from database import SessionLocal
from starlette import status
from pydantic import BaseModel

from models import Users,Followers
from routers.auth import get_current_user


router = APIRouter (
    prefix = '/followers',
    tags = ['followers']
)


@router.post("/follow",status_code=status.HTTP_204_NO_CONTENT)
async def follow_user():
    pass


@router.post("/unfollow",status_code=status.HTTP_204_NO_CONTENT)
async def unfollow_user():
    pass

@router.get("/get_followers",status_code=status.HTTP_200_OK)
async def get_followers():
    pass

@router.get("/get_followings",status_code=status.HTTP_200_OK)
async def get_followings():
    pass
