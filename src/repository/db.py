# For simplicity's sake, we don´t do migrations
from contextlib import contextmanager
from typing import TypeVar, Generator, Type

from pydantic import BaseModel
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

from src import config
from .model._base import Base  # noqa

_T = TypeVar("_T")
_Q = TypeVar("_Q", bound=BaseModel)

db: Engine
session_maker: sessionmaker


def init(db_url: str = config.DB_NAME, *, debug: bool = config.DB_ECHO) -> None:
    global db, session_maker

    db = create_engine(db_url, connect_args={"check_same_thread": False})
    db.echo = debug
    Base.metadata.create_all(db)  # to be replaced by alembic migrations
    session_maker = sessionmaker(bind=db, autoflush=False, autocommit=False)


@contextmanager
def new_session() -> Generator[Session, None, None]:
    session = session_maker()
    try:
        yield session
    finally:
        session.close()


def generic_create(model_instance: _T, domain_class: Type[_Q]) -> _Q:
    with new_session() as session:
        session.add(model_instance)
        session.commit()
        session.refresh(model_instance)

        return domain_class.from_orm(model_instance)


def generic_get(id: int, model_instance: _T, domain_class: Type[_Q]) -> _Q:
    with new_session() as session:
        return domain_class.from_orm(session.get(model_instance, id))
