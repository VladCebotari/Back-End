from typing import Annotated

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException,Depends
from database import SessionLocal
from starlette import status
from pydantic import BaseModel

from models import Users,Followers
from routers.auth import get_current_user


router = APIRouter (
    prefix = '/followers',
    tags = ['followers']
)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]

@router.post("/follow/{followed_id}",status_code=status.HTTP_201_CREATED)
async def follow_user(user : user_dependency,
                      db : db_dependency,
                      followed_id : int):
    if user is None:
        raise HTTPException(status_code=401,detail="Not authenticated")
    if user.get("id") == followed_id:
        raise HTTPException(status_code=400,detail="You can't follow yourself")

    new_follow = Followers (
        follower_id = user.get("id"),
        followed_id = followed_id
    )
    try:
        db.add(new_follow)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=409,detail="You are already following this user")

    return {"message": "You are now following the user."}

@router.post("/unfollow",status_code=status.HTTP_204_NO_CONTENT)
async def unfollow_user():
    pass

@router.get("/get_followers",status_code=status.HTTP_200_OK)
async def get_followers():
    pass

@router.get("/get_followings",status_code=status.HTTP_200_OK)
async def get_followings():
    pass
