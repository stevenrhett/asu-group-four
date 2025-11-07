from beanie import Document
from pydantic import BaseModel, EmailStr
from typing import Literal


class User(Document):
    email: EmailStr
    hashed_password: str
    role: Literal["seeker", "employer"]

    class Settings:
        name = "users"


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Literal["seeker", "employer"]


class UserPublic(BaseModel):
    id: str
    email: EmailStr
    role: Literal["seeker", "employer"]

