from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.types import Info

from troczone_api import models
from troczone_api.schemas.lazy import UserSchema


async def me(info: Info) -> UserSchema:
    current_user: models.User = info.context["current_user"]

    return current_user