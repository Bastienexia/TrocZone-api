from strawberry.types import Info

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from troczone_api.models import User, Authentication
from troczone_api.schemas.lazy import UserSchema
from troczone_api.schemas.users import ChangePassword
from troczone_api.core.security import verify_password, get_password_hash


async def change_password(info: Info, passwords: ChangePassword) -> UserSchema:
    session: AsyncSession = info.context["session"]
    current_user: User = info.context["current_user"]

    auth = (await session.execute(Authentication.select().filter(Authentication.user_id == current_user.id))).scalar_one()

    if verify_password(passwords.old_password, auth.hashed_password) is False:
        return

    auth.hashed_password = get_password_hash(passwords.new_password)
    session.add(auth)

    await session.commit()

    return current_user


async def delete_account(info: Info, password: str) -> UserSchema:
    session: AsyncSession = info.context["session"]
    current_user: User = info.context["current_user"]

    auth = (await session.execute(Authentication.select().filter(Authentication.user_id == current_user.id))).scalar_one()

    if verify_password(password, auth.hashed_password) is False:
        return

    current_user.deleted_at = datetime.utcnow()
    auth.deleted_at = datetime.utcnow()

    session.add(current_user)
    session.add(auth)

    await session.commit()

    return current_user


async def update_user(info: Info, password: str, email: str | None = None, phone_number: str | None = None) -> UserSchema:
    session: AsyncSession = info.context["session"]
    current_user: User = info.context["current_user"]

    auth = (await session.execute(Authentication.select().filter(Authentication.user_id == current_user.id))).scalar_one()

    if verify_password(password, auth.hashed_password) is False:
        return

    if email:
        current_user.email = email
    if phone_number:
        current_user.phone_number = phone_number

    session.add(current_user)

    await session.commit()

    return current_user