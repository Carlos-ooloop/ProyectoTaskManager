from db.database import engine
from models.user_model import User
from fastapi import FastAPI
from Routers import Task_CRUD, users_CRUD
from utils import auth

User.metadata.create_all(bind = engine)

app = FastAPI()

app.include_router(Task_CRUD.router)
app.include_router(users_CRUD.router)
app.include_router(auth.router)




