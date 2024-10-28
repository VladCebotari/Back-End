from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
# from dotenv import load_dotenv

# load_dotenv()
os.getenv('SQLALCHEMY_DATABSE_URL')
SQLALCHEMY_DATABSE_URL = os.getenv('SQLALCHEMY_DATABSE_URL')

engine=create_engine(SQLALCHEMY_DATABSE_URL)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()




