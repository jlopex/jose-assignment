# For simplicity's sake, we don´t do migrations
from contextlib import contextmanager
from typing import TypeVar, Generator

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

from src import config
from .model._base import Base  # noqa

_T = TypeVar("_T")

db: Engine
session_maker: sessionmaker


def init(db_url: str = config.DB_NAME) -> None:
    global db, session_maker

    db = create_engine(db_url, connect_args={"check_same_thread": False})
    db.echo = config.DB_ECHO
    Base.metadata.create_all(db)  # to be replaced by alembic migrations
    session_maker = sessionmaker(bind=db, autoflush=False, autocommit=False)


@contextmanager
def new_session() -> Generator[Session, None, None]:
    session = session_maker()
    try:
        yield session
    finally:
        session.close()


def generic_create(model_instance: _T) -> _T:
    with new_session() as session:
        session.add(model_instance)
        session.commit()
        session.refresh(model_instance)

        return model_instance
