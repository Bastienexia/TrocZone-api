from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.types import Info
import strawberry
from datetime import datetime

from troczone_api import models
from troczone_api.schemas import Post, CreatePost, UpdatePost


async def create_post(info: Info, post: CreatePost) -> Post:
    session: AsyncSession = info.context["session"]
    current_user: models.User = info.context["current_user"]

    post = models.Post(
        name=post.name,
        price=post.price,
        description=post.description,
        characteristic=post.characteristic,
        pictures=post.pictures,
        creator_id=current_user.id
    )

    session.add(post)

    await session.commit()

    return post


async def update_post(info: Info, update_post: UpdatePost, post_id: strawberry.ID) -> Post:
    session: AsyncSession = info.context["session"]
    current_user: models.User = info.context["current_user"]

    post = (await session.execute(models.Post.select().filter(models.Post.id == int(post_id)))).scalar_one()

    if update_post.name:
        post.name = update_post.name
    if update_post.price:
        post.price = update_post.price
    if update_post.description:
        post.description = update_post.description
    if update_post.characteristic:
        post.characteristic = update_post.characteristic
    if update_post.pictures:
        post.pictures = update_post.pictures

    session.add(post)

    await session.commit()

    return post


async def delete_post(info: Info, post_id: strawberry.id) -> Post:
    session: AsyncSession = info.context["session"]
    current_user: models.User = info.context["current_user"]

    post = (await session.execute(models.Post.select().filter(models.Post.id == int(post_id)))).scalar_one()

    if post.creator_id != current_user.id:
        return

    post.deleted_at = datetime.utcnow()

    session.add(post)

    await session.commit()

    return post
