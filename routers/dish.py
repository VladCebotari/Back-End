from typing import Annotated


from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,HTTPException,Path,UploadFile,File
from database import SessionLocal
from starlette import status
from pydantic import BaseModel,Field

from models import Users,Dish
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


class DishRequest(BaseModel):
    name: str
    description : str
    ingredients : str


@router.post("/dishes",status_code=status.HTTP_201_CREATED)
async def post_dish(user : user_dependency,
                    db: db_dependency,
                    image : UploadFile = File(...),
                    dish_request : DishRequest = Depends()):

    if user is None:
        raise HTTPException(status_code=401, detail="authentication failed")

    user_image = await image.read()
    user_image_base64 = base64.b64encode(user_image).decode("utf-8")

    create_dish_model = Dish (
        user_id = user.get("id"),
        image = user_image_base64,
        name = dish_request.name,
        description = dish_request.description,
        ingredients = dish_request.ingredients
    )

    db.add(create_dish_model)
    db.commit()

    return {"message": "Dish posted successfully"}





