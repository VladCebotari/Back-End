from email.policy import default

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
    likes = relationship("Like", back_populates="user")

    followers = relationship(
        "Followers",
        back_populates="followed",
        foreign_keys=[Followers.followed_id],
        cascade="all, delete"
    )

    # Relationship for users whom this user is following
    following = relationship(
        "Followers",
        back_populates="follower",
        foreign_keys=[Followers.follower_id],
        cascade="all, delete"
    )

class Dish(Base):
    __tablename__ = 'dish'

    dish_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    ingredients = Column(Text)
    image = Column(String)
    like_count = Column (Integer, default=0)

    user = relationship("Users", back_populates="dishes")
    reviews = relationship("Review", back_populates="dish")
    ratings = relationship("Rating", back_populates="dish")
    likes = relationship("Like",back_populates="dish",cascade="all,delete")



class Like(Base):
    __tablename__ = 'like'

    like_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    dish_id = Column(Integer, ForeignKey('dish.dish_id'), nullable=False)

    user = relationship("Users", back_populates="likes")
    dish = relationship("Dish", back_populates="likes")

    __table_args__ = (UniqueConstraint('user_id', 'dish_id', name='unique_user_dish_like'),)


class Followers(Base):
    __tablename__ = 'followers'
    connection_id = Column(Integer, primary_key=True, autoincrement=True)
    follower_id = Column(Integer,ForeignKey('users.id'),nullable=False)
    followed_id = Column(Integer,ForeignKey('users.id'),nullable=False)
    timestamp = Column (DateTime(timezone=True), default=func.now)

    follower = relationship("Users", back_populates="followers", foreign_keys=[follower_id])
    followed = relationship("Users", back_populates="following", foreign_keys=[followed_id])

    __tableargs__ = (UniqueConstraint('follower_id', 'followed_id', name='unique_follower_followed_connection'),)


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
