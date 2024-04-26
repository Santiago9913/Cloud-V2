from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from dtos.auth import SignUpDto
from sqlmodel import Session
from utils.db_engine import get_session
from models.models import User
from jose import jwt
from utils.auth_utils import OAuth2_scheme
from env import JWT_SECRET_KEY, ALGORITHM

router = APIRouter(
    prefix="/users",
)


@router.get("/", tags=["users"])
async def getUser(token: Annotated[str, Depends(OAuth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token=token,
            key=JWT_SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        print(payload)
    except:
        raise credentials_exception


async def createUser(*, user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
