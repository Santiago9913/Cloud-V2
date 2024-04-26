from sqlmodel import create_engine, Session
from env import (
    POSTGRES_HOST,
    POSTGRES_DB,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    ENV,
)

engine = None


def init_engine():
    global engine
    engine = create_engine(
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}",
        echo=True,
    )
    return engine


def get_session():
    if not engine:
        raise Exception("Engine not initialized")
    else:
        with Session(engine) as session:
            yield session
