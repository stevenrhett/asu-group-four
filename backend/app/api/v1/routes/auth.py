from fastapi import APIRouter, HTTPException
from fastapi import Depends
from pydantic import EmailStr

from app.models.user import User, UserCreate
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter()


@router.post("/register")
async def register(payload: UserCreate):
    exists = await User.find_one(User.email == payload.email)
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=payload.email, hashed_password=hash_password(payload.password), role=payload.role)
    await user.insert()
    return {"id": str(user.id), "email": user.email, "role": user.role}


class LoginPayload(UserCreate):
    pass


@router.post("/login")
async def login(payload: LoginPayload):
    user = await User.find_one(User.email == payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(subject=str(user.id), extra={"role": user.role})
    return {"access_token": token, "token_type": "bearer"}

