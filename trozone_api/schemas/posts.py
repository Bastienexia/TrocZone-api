import strawberry

from trozone_api.schemas.base import BaseSchema


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
