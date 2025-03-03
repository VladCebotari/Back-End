from fastapi import FastAPI
from database import engine
import uvicorn
import models
from routers import auth,todos,admin,users,account,dish,followers
from fastapi.middleware.cors import CORSMiddleware


app=FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(account.router)
app.include_router(dish.router)
app.include_router(followers.router)

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)

