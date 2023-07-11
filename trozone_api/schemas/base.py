from typing import Generic, TypeVar

import strawberry
from strawberry.annotation import StrawberryAnnotation

GenericType = TypeVar("GenericType")


@strawberry.type
class Connection(Generic[GenericType]):
    page_info: "PageInfo"
    total_count: int
    edges: list["Edge[GenericType]"]


@strawberry.type
class PageInfo:
    has_previous_page: bool
    has_next_page: bool
    start_cursor: str | None
    end_cursor: str | None


@strawberry.type
class Edge(Generic[GenericType]):
    node: GenericType
    cursor: str


class BaseSchema:
    @classmethod
    def from_model(cls, model):
        values= {}
        for k, v in cls.__annotations__.items():
            if not isinstance(v, StrawberryAnnotation):
                if hasattr(model, k):
                    values[k] = getattr(model, k)
        return cls(**values)
