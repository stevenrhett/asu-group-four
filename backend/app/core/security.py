from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class InvalidTokenError(Exception):
    """Raised when a JWT cannot be decoded or validated."""


class TokenPayload(BaseModel):
    sub: str
    role: str
    exp: int


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str, expires_minutes: int = 60, extra: Optional[dict] = None) -> str:
    to_encode = {"sub": subject, "exp": datetime.utcnow() + timedelta(minutes=expires_minutes)}
    if extra:
        to_encode.update(extra)
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        return TokenPayload(**payload)
    except (JWTError, ValidationError) as exc:
        raise InvalidTokenError(str(exc)) from exc
