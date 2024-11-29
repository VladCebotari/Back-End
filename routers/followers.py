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

@router.post("/follow/{username}",status_code=status.HTTP_201_CREATED)
async def follow_user(user : user_dependency,
                      db : db_dependency,
                      username : str):

    if user is None:
        raise HTTPException(status_code=401,detail="Not authenticated")

    existing_user = db.query(Users).filter(Users.username == username).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="The user you're trying to follow doesn't exist")

    followed_id = db.query(Users.id).filter(Users.username == username).first()[0]
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

@router.post("/unfollow/{username}",status_code=status.HTTP_204_NO_CONTENT)
async def unfollow_user(user : user_dependency,
                        db: db_dependency,
                        username : str):
    if user is None:
        raise HTTPException(status_code=401,detail="Not authenticated")
    existing_user = db.query(Users).filter(Users.username == username).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="The user you're trying to unfollow doesn't exist")
    followed_id = db.query(Users.id).filter(Users.username == username).first()[0]
    existing_follow = db.query(Users).filter(user.get("id") == Followers.follower_id,followed_id == Followers.followed_id).first()
#     db something etc...
@router.get("/get_followers",status_code=status.HTTP_200_OK)
async def get_followers():
    pass

@router.get("/get_followings",status_code=status.HTTP_200_OK)
async def get_followings():
    pass
