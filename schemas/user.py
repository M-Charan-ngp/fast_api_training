from pydantic import BaseModel
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class UserCreate(BaseModel):
    username: str
    password: str
    role: UserRole = UserRole.USER

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    username: str
    password: str