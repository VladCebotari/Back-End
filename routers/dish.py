from typing import Annotated

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,HTTPException,UploadFile,File,Form,Query
from starlette.responses import JSONResponse

from database import SessionLocal
from starlette import status
from pydantic import BaseModel

from models import Dish, Like
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
        ingredients = ingredients,
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

    return JSONResponse(content=[{
        "dish_id": dish.dish_id,
        "user_id": dish.user_id,
        "name": dish.name,
        "description": dish.description,
        "ingredients": dish.ingredients,
        "image": dish.image
    } for dish in dishes])

@router.post("/dishes/{dish_id}/like",status_code=status.HTTP_201_CREATED)
async def like_dish (user : user_dependency,
                     db : db_dependency,
                     dish_id : int ):
    dish = db.query(Dish).filter(Dish.dish_id == dish_id ).first()
    if not dish:
        raise HTTPException(status_code=404,detail="Dish not found")

    existing_like = db.query(Like).filter(Like.dish_id == dish_id,Like.user_id == user.get("id") ).first()
    if existing_like:
        raise HTTPException(status_code=400,detail="You already liked this dish")

    try:
        new_like = Like(dish_id=dish_id, user_id=user.get("id"))
        db.add(new_like)
        # Increment like_count safely
        db.query(Dish).filter(Dish.dish_id == dish_id).update(
            {"like_count": Dish.like_count + 1},
            synchronize_session="fetch"
        )
        db.commit()
        db.refresh(dish)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to like the dish. Please try again.")

    return {"message": "Dish liked successfully", "like_count": dish.like_count}
