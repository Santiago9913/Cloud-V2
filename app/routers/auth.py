from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from dtos.auth import SignInDto, SignUpDto
from utils.auth_utils import pwd_context
from utils.db_engine import get_session
from utils.auth_utils import pwd_context
from sqlmodel import Session, select
from models.models import User
from .users import createUser, getUser
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from env import JWT_SECRET_KEY, ALGORITHM

router = APIRouter(
    prefix="/auth",
)


@router.post("/signin", tags=["auth"])
async def signIn(*, session: Session = Depends(get_session), dto: SignInDto):
    user = authenticate_user(
        session=session, email=dto.email, password=dto.password
    ).model_dump(exclude={"password"})
    access_token = create_access_token(user=user, expires_delta=timedelta(minutes=15))
    res = jsonable_encoder(
        {"access_token": access_token, "token_type": "bearer", "user": user}
    )
    return JSONResponse(content=res)


@router.post("/signup", tags=["auth"])
async def signUp(*, session: Session = Depends(get_session), dto: SignUpDto):

    user = session.exec(select(User).where(User.email == dto.email)).first()
    if not user:
        user = User(
            email=dto.email,
            name=dto.name,
            password=get_password_hash(dto.password),
        )
        await createUser(session=session, user=user)
        return user
    else:
        raise HTTPException(status_code=400, detail="User already exists")


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(session: Session, email: str, password: str):
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(
            status_code=400, detail="User not found or incorrect password"
        )
    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=400, detail="User not found or incorrect password"
        )
    return user


def create_access_token(user: User, expires_delta: timedelta | None):
    to_encode = user
    if expires_delta:
        uuid = str(to_encode.get("id"))
        to_encode["id"] = uuid
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
