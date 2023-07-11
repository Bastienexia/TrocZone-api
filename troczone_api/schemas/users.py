import strawberry

from troczone_api.schemas.base import BaseSchema


@strawberry.type
class User(BaseSchema):
    id: int
    firstname: str
    name: str
    birthdate: str
    email: str
    phone_number: str | None
    profile_picture: str | None
