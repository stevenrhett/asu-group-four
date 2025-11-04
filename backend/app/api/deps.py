from typing import Callable, Literal

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.security import decode_access_token, InvalidTokenError, TokenPayload
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload: TokenPayload = decode_access_token(token)
    except InvalidTokenError as exc:  # pragma: no cover - defensive branch
        raise credentials_error from exc

    user = await User.get(payload.sub)
    if not user:
        raise credentials_error
    if user.role != payload.role:
        # Reject tokens where the role claim no longer matches persisted role
        raise credentials_error
    return user


def require_role(*roles: Literal["seeker", "employer"]) -> Callable[[User], User]:
    async def role_dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user

    return role_dependency
