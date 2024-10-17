from fastapi import FastAPI
from database import engine

import models
from routers import auth,todos,admin,users,account

app=FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(account.router)


#dependencies - (toate librariile)
#postgresql - baza de date
#sql alchemy connection with postgresql
#Route de profile

