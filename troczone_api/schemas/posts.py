import strawberry

from troczone_api.schemas.base import BaseSchema


@strawberry.type
class Post(BaseSchema):
    id: int
    name: str
    price: float
    description: str | None
    characteristic: list[dict] | None
    state: str
    creator_id: int
    pictures: list[str] | None


@strawberry.input
class CreatePost(BaseSchema):
    name: str
    price: float
    description: str | None
    characteristic: list[dict] | None
    pictures: list[str] | None


@strawberry.input
class UpdatePost(BaseSchema):
    name: str | None
    price: float | None
    description: str | None
    characteristic: list[dict] | None
    pictures: list[str] | None
