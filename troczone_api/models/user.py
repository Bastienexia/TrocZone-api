from sqlalchemy import Column, Integer, ForeignKey, String, Date, LargeBinary
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from troczone_api.models.base import BaseTable, Base


class User(BaseTable):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    firstname = Column("firstname", String, nullable=False)
    name = Column("name", String, nullable=False)
    birthdate = Column("birthdate", Date, nullable=False)
    email = Column("email", String, nullable=False)
    phone_number = Column("phone_number", String, nullable=True)
    profile_picture = Column("profile_picture", LargeBinary, nullable=True)

    authentications = relationship("Authentication", back_populates="user")
    posts = relationship("Post", back_populates="user")
    savedposts = relationship("UserSavedPost", back_populates="user")

    @hybrid_property
    def password(self):
        password = self.authentications
        return password


class UserSavedPost(Base):
    __tablename__ = "user_saved_post"

    user_id = Column("user_id", Integer, ForeignKey("users.id"), primary_key=True)
    post_id = Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True)

    user = relationship("User", back_populates="savedposts")
    post = relationship("Post", back_populates="savedposts")
