from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.types import Info
import strawberry

from troczone_api import models
from troczone_api.schemas import Connection, Edge, PageInfo
from troczone_api.schemas.lazy import PostSchema
from troczone_api.lib.sqlakeyset.paging import get_page
from troczone_api.lib.sqlakeyset.results import unserialize_bookmark

async def get_post(info: Info, post_id: strawberry.ID) -> PostSchema:
    session: AsyncSession = info.context["session"]

    post = (await session.execute(models.Post.select().filter(models.Post.id == int(post_id)))).scalar_one()

    return post


async def get_posts(info: Info, first: int = 25, after: str | None = None, before: str | None = None) -> Connection[PostSchema]:
    session: AsyncSession = info.context["session"]

    query = models.Post.select()
    count_query = models.Post.select_count()

    total_count = await session.scalar(count_query)
    if after is not None:
        place, _ = unserialize_bookmark(after)
        page = await get_page(session, query, first, place, False)
    elif before is not None:
        place, _ = unserialize_bookmark(before)
        page = await get_page(session, query, first, place, True)
    else:
        page = await get_page(session, query, first, None, False)

    edges = [
        Edge(
            node=m,
            cursor=page.paging.get_marker_at(i)
        )
        for i, (m,) in enumerate(page)
    ]

    return Connection(
        page_info=PageInfo(
            has_previous_page=page.paging.has_previous,
            has_next_page=page.paging.has_next,
            start_cursor=page.paging.bookmark_previous,
            end_cursor=page.paging.bookmark_next
        ),
        total_count=total_count,
        edges=edges
    )