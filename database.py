from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABSE_URL='postgresql://postgres:ciociosan@localhost/CodeChefsDataBase'

engine=create_engine(SQLALCHEMY_DATABSE_URL)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()




