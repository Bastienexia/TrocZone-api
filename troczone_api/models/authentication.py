from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from troczone_api.models.base import BaseTable


class Authentication(BaseTable):
    __tablename__ = "authentications"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    user_id = Column("user_id", Integer, ForeignKey("users.id"), nullable=False)
    hashed_password = Column("hashed_password", String(255), nullable=False)

    user = relationship("User", back_populates="authentications")

    def __repr__(self):
        return f"<Authentication[{self.type}](id=|{self.id}|)"
