from database import Base
from sqlalchemy import Column,Integer,String,BOOLEAN,ForeignKey

class Users(Base):
    __tablename__='users'

    id = Column(Integer,primary_key=True,index=True)
    email = Column(String,unique=True)
    username = Column(String,unique=True)
    firstname = Column(String)
    lastname = Column(String)
    hashed_password = Column(String)
    is_active = Column(BOOLEAN,default=True)
    role = Column(String)
    phone_number=Column(String)
    # public_id = Column(uuid())


class Todos(Base):
    __tablename__= 'todos'

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(BOOLEAN,default=False)
    owner = Column(Integer,ForeignKey("users.id"))