import enum
from sqlmodel import Field, SQLModel, Relationship
from uuid import uuid4, UUID
from typing import Optional
from uuid import uuid4, UUID
from sqlalchemy import Column, String
from sqlalchemy_utils import ChoiceType


class User(SQLModel, table=True):
    id: UUID = Field(default=uuid4, primary_key=True, unique=True)
    name: str = Field(max_length=50)
    email: str = Field(max_length=50, unique=True, primary_key=False)
    password: str = Field(max_length=50)
    tasks: list["Task"] = Relationship(back_populates="user")

    class Config:
        frozen = True


class TaskStatus(enum.Enum):
    UPLOADED = ("uploaded",)
    PENDING = ("pending",)
    COMPLETED = "completed"


class Task(SQLModel, table=True):
    id: UUID = Field(default=uuid4(), primary_key=True)
    status: TaskStatus = Field(
        sa_column=Column(ChoiceType(TaskStatus, impl=String()), nullable=False)
    )
    user_id: Optional[UUID] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="tasks")
