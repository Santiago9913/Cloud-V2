from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from fastapi.security import OAuth2PasswordBearer
from contextlib import asynccontextmanager

from utils.db_engine import init_engine
from utils.cloud_storage import init_cludstorage
from env import ENV

from routers.auth import router as auth_router
from routers.tasks import router as tasks_router
from routers.users import router as users_router

import uvicorn
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_cludstorage()
    engine = init_engine()
    SQLModel.metadata.create_all(engine)

    yield


app = FastAPI(lifespan=lifespan, debug=ENV == "development")
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(users_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=int(os.environ.get("PORT", 8000)))
