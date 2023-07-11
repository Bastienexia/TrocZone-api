from datetime import datetime, timedelta
from secrets import token_urlsafe

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.future import select

from trozone_api import models
from trozone_api.core.config import settings, redis
from trozone_api.schemas.auth import Token

ALGORITHM = "HS256"

pwd_context = CryptContext(schemes="bcrypt", deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(session, user_id: int):
    user = await session.scalar(
        select(models.User).filter(models.User.id == user_id).filter(models.User.deleted_at == None)
    )
    return user


async def get_user_by_email(session, email: str):
    user = await session.scalar(models.User).filter(models.User.email == email).filter(models.User.deleted_at == None)
    return user


async def authenticate_user(session, user_id: int, password: str):
    auth = await session.scalar(
        select(models.Authentication).filter(models.Authentication.user_id == user_id).filter(models.Authentication.deleted_at == None)
    )
    if not verify_password(password, auth.hashed_password):
        return False
    return True


def create_access_token(data: dict, expire_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MIUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expire_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_token(user_id: int):
    refresh_token = token_urlsafe(32)
    access_token =create_access_token({"sub": str(user_id)})
    redis.set(
        f"refresh_token:{refresh_token}",
        user_id,
        ex=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60
    )
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MIUTES * 60
    )