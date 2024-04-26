from pydantic import BaseModel, EmailStr


class SignUpDto(BaseModel):
    name: str
    email: EmailStr
    password: str


class SignInDto(BaseModel):
    email: str
    password: str
