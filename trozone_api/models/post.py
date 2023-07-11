from sqlalchemy import Column, Integer, ForeignKey, LargeBinary, JSON, String, TEXT, FLOAT, ARRAY
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from trozone_api.models.base import BaseTable, Base


class Post(BaseTable):
    __tablename__ = "posts"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String, nullable=False)
    price = Column("price", FLOAT, nullable=False)
    description = Column("description", TEXT, nullable=True)
    characteristic = Column("characteristic", ARRAY(item_type=JSON), nullable=True)
    state = Column("state", String, nullable=False)
    creator_id = Column("creator_id", Integer, ForeignKey("users.id"), nullable=False)
    pictures = Column("pictures", ARRAY(item_type=LargeBinary), nullable=True)

    user = relationship("User", back_populates="posts")
    savedposts = relationship("UserSavedPost", back_populates="post")
    