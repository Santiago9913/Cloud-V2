import os

POSTGRES_USER = os.getenv("POSTGRES_USER", default="postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", default="password")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", default="localhost")
POSTGRES_DB = os.getenv("POSTGRES_DB", default="dbIDRL")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", default=4345)