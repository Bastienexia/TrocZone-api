from sqlalchemy import TIMESTAMP, Column, func
from sqlalchemy.future import select
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

from trozone_api.db.session import sync_engine

Base = declarative_base()

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)
)

Base.query = db_session.query_property()


class BaseTable(Base):
    __abstract__ = True

    deleted_at = Column("deleted_at", TIMESTAMP(timezone=True))

    @classmethod
    def select(cls):
        return select(cls).filter(cls.deleted_at == None)

    @classmethod
    def select_count(cls):
        return select(func.count()).select_from(cls).filter(cls.deleted_at == None)
