from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel

from troczone_api.core.config import settings
from troczone_api.core.security import ALGORITHM, oauth2_scheme, get_user
from troczone_api.db.session import get_session

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/login")


class TokenPayload(BaseModel):
    sub: int | None = None


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user(
    token: str = Depends(oauth2_scheme), session=Depends(get_session())
):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user(session, user_id)

    if user is None:
        raise credentials_exception
    return user
