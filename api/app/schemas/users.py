from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from enum import Enum


class UserCreate(BaseModel):
    firstname: str
    lastname: Optional[str] = None
    phone: str
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)



class UserRead(BaseModel):
    id: int
    firstname: str
    lastname: Optional[str] = None
    email: EmailStr
    phone: str
    role: Optional[str] = None
    is_active: bool
    is_superuser: bool

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class TokenPayload(BaseModel):
    sub: str
    exp: float
    iat: float
    type: str