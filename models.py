from database import Base
from sqlalchemy import Column, Integer, String, BOOLEAN, ForeignKey, Text, DateTime, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    firstname = Column(String)
    lastname = Column(String)
    hashed_password = Column(String)
    is_active = Column(BOOLEAN, default=True)
    role = Column(String)
    phone_number = Column(String)

    dishes = relationship("Dish", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    ratings = relationship("Rating", back_populates="user")


class Dish(Base):
    __tablename__ = 'dish'

    dish_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    ingredients = Column(Text)
    instructions = Column(Text)
    image = Column(String)

    user = relationship("Users", back_populates="dishes")  # Changed to Users
    reviews = relationship("Review", back_populates="dish")
    ratings = relationship("Rating", back_populates="dish")


class Review(Base):
    __tablename__ = 'review'

    review_id = Column(Integer, primary_key=True, autoincrement=True)
    dish_id = Column(Integer, ForeignKey('dish.dish_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    review_text = Column(Text)
    review_date = Column(DateTime, server_default=func.now())

    dish = relationship("Dish", back_populates="reviews")
    user = relationship("Users", back_populates="reviews")  # Changed to Users

    __table_args__ = (UniqueConstraint('dish_id', 'user_id', name='unique_dish_user_review'),)


class Rating(Base):
    __tablename__ = 'rating'

    rating_id = Column(Integer, primary_key=True, autoincrement=True)
    dish_id = Column(Integer, ForeignKey('dish.dish_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    rating_value = Column(Integer, CheckConstraint('rating_value BETWEEN 1 AND 5'))

    dish = relationship("Dish", back_populates="ratings")
    user = relationship("Users", back_populates="ratings")  # Changed to Users

    __table_args__ = (UniqueConstraint('dish_id', 'user_id', name='unique_dish_user_rating'),)

class Todos(Base):
    __tablename__= 'todos'

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(BOOLEAN,default=False)
    owner = Column(Integer,ForeignKey("users.id"))
