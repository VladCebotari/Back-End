from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from starlette import status
from fastapi import Depends
from typing import Annotated
from .auth import get_current_user
import base64

from models import Users,Dish,Notifications
from database import SessionLocal

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


@router.get("/get_all_posts",status_code=status.HTTP_200_OK)
async def see_all_dishes(user:user_dependency,
                         db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail="authentication failed")
    all_users_dishes = db.query(Dish).filter(Dish.user_id == user.get("id")).all()
    return all_users_dishes

@router.get("/get_profile_picture",status_code=status.HTTP_200_OK)
async def see_all_dishes(user:user_dependency,
                         db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail="authentication failed")
    profile_picture = db.query(Users.profile_picture).filter(user.get("id") == Users.id).scalar()
    return profile_picture


@router.post("/add_profile_picture",status_code=status.HTTP_201_CREATED)
async def add_profile_picture (user: user_dependency,
                               db : db_dependency,
                               profile_picture_image: UploadFile = File(...)):
    if user is None:
        raise HTTPException(status_code=401,detail="authentication failed")

    if profile_picture_image.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    pfp = await profile_picture_image.read()
    pfp_base64 = base64.b64encode(pfp).decode("utf-8")

    user_information = db.query(Users).filter(Users.id == user.get("id")).first()
    user_information.profile_picture = pfp_base64

    try:
        db.add(user_information)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=500,detail=f"Unexpected error {str(e)}")

    return {"message": "Image updated successfully "}

@router.get("/get_notifications",status_code=status.HTTP_200_OK)
async def get_notifications(user : user_dependency,
                            db : db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail="authentication failed")

    all_notifications = db.query(Notifications.notification_content,Notifications.seen,Notifications.timestamp).filter(user.get("id") == Notifications.receiver_user_id).all()

    result = [dict(zip(['notification_content','seen', 'timestamp'], row)) for row in all_notifications]

    return jsonable_encoder(result)