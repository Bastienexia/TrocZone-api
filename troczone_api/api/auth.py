from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from troczone_api import models
from troczone_api.core.config import redis
from troczone_api.core.security import (
    pwd_context,
    get_user_by_email,
    authenticate_user,
    create_token,
)
from troczone_api.db.session import get_session
from troczone_api.schemas.auth import Token, OAuth2TokenForm, UserCreate

router = APIRouter()


async def login(session, data):
    user = await get_user_by_email(session, data.username)
    if (not user) or (not await authenticate_user(session, user.id, data.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return create_token(user.id)


async def refresh(data):
    key = f"refresh_token:{data.refresh_token}"
    user_id = redis.get(key)
    redis.delete(key)
    if user_id is None:
        HTTPException(401, "Invalid refresh_token")

    return create_token(int(user_id))


@router.post("/token", response_model=Token)
async def login_token(
    form_data: OAuth2TokenForm = Depends(), session=Depends(get_session)
):
    if form_data.grant_type == "password":
        return await login(session, form_data)
    else:
        return await refresh(form_data)


@router.post("/signup")
async def signup(obj_in: UserCreate, session: AsyncSession = Depends(get_session)):
    existing_user = await session.scalar(
        select(models.User)
        .filter(models.User.email == obj_in.email)
        .filter(models.User.deleted_at == None)
    )
    if existing_user:
        raise HTTPException(400, "This email is already associated with an account.")

    user = models.User(email=obj_in.email)
    user.authentications.append(
        models.Authentication(hashed_password=pwd_context.hash(obj_in.password))
    )

    session.add(user)
    await session.commit()

    return {"success": True}
