from pydantic import BaseModel, EmailStr
from enum import Enum

class UserRole(str, Enum):
    patient = "patient"
    admin = "admin"

class User(BaseModel):
    name: str
    email: EmailStr
    role: UserRole = UserRole.patient

class UserDB(User):
    id: int
    class Config:
        orm_mode = True

class UserRegister(User):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class RegisterResponse(BaseModel):
    message: str
    data: UserDB

class LoginResponse(BaseModel):
    message: str
    data: UserDB
    access_token: str
    token_type: str

class LogoutResponse(BaseModel):
    message: str