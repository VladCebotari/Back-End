from typing import Annotated

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,HTTPException,UploadFile,File,Form,Query
from starlette.responses import JSONResponse

from database import SessionLocal
from starlette import status
from pydantic import BaseModel

from models import Dish
from routers.auth import get_current_user
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




@router.post("/dishes",status_code=status.HTTP_201_CREATED)
async def post_dish(user : user_dependency,
                    db: db_dependency,
                    image : UploadFile = File(...),
                    name : str = Form(...),
                    description : str = Form(...),
                    ingredients : str = Form(...)
                    ):

    if user is None:
        raise HTTPException(status_code=401, detail="authentication failed")

    user_image = await image.read()
    user_image_base64 = base64.b64encode(user_image).decode("utf-8")

    create_dish_model = Dish (
        user_id = user.get("id"),
        image = user_image_base64,
        name = name,
        description = description,
        ingredients = ingredients
    )

    db.add(create_dish_model)
    db.commit()

    return {"message": "Dish posted successfully"}



@router.get("/search",status_code=status.HTTP_200_OK)
async def search_dishes(user : user_dependency,
                        db: db_dependency,
                        name : str = Query(...)
                        ):
    if user is None:
        raise HTTPException(status_code=401,detail="authentication failed")

    search_term = f"%{name}%"
    try:
        dishes = db.query(Dish).filter(Dish.name.ilike(search_term)).all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database query error") from e


    # return JSONResponse(content=[dish[0] for dish in dishes])
    return JSONResponse(content=[{
        "dish_id": dish.dish_id,
        "user_id": dish.user_id,
        "name": dish.name,
        "description": dish.description,
        "ingredients": dish.ingredients,
        "image": dish.image
    } for dish in dishes])