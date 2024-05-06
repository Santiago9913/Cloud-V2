from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from dtos.auth import SignUpDto
from sqlmodel import Session, select
from utils.db_engine import get_session
from models.models import User
from jose import jwt, JWTError
from utils.auth_utils import OAuth2_scheme
from env import JWT_SECRET_KEY, ALGORITHM

router = APIRouter(
    prefix="/users",
)


@router.get("/", tags=["users"])
async def getUser(
    token: Annotated[str, Depends(OAuth2_scheme)],
    session: Session = Depends(get_session),
):
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
        email: str = payload.get("email")
        if email is None:

            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = session.exec(select(User).where(User.email == email)).first()
    if user is None:
        raise credentials_exception
    return user.model_dump(exclude={"password"})


async def createUser(*, user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
