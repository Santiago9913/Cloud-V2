from fastapi import FastAPI
from sqlmodel import SQLModel
from fastapi.security import OAuth2PasswordBearer
from contextlib import asynccontextmanager

from utils.db_engine import init_engine
from env import ENV

from routers.auth import router as auth_router
from routers.tasks import router as tasks_router
from routers.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = init_engine()
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan, debug=ENV == "development")

app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(users_router)
