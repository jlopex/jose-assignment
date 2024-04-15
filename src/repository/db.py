# For simplicity's sake, we don´t do migrations
from contextlib import contextmanager
from typing import TypeVar, Generator, Type

from pydantic import BaseModel
from sqlalchemy import create_engine, Engine, StaticPool
from sqlalchemy.orm import sessionmaker, Session

from src import config
from .model._base import Base  # noqa

_T = TypeVar("_T")
_Q = TypeVar("_Q", bound=BaseModel)

db: Engine
session_maker: sessionmaker


def init(db_url: str = config.DB_NAME, *, debug: bool = config.DB_ECHO) -> None:
    global db, session_maker

    db = create_engine(
        db_url, connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
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
    from .exceptions import RepositoryNotFoundError

    with new_session() as session:
        model = session.get(model_instance, id)
        if model is None:
            raise RepositoryNotFoundError(f"Model {model_instance}[{id}] not found")

        return domain_class.from_orm(model)


def generic_list(model_instance: _T, domain_class: Type[_Q], **kwargs) -> list[_Q]:
    with new_session() as session:
        models = session.query(model_instance).filter_by(**kwargs).all()
        return [domain_class.from_orm(model) for model in models]


def generic_delete(model_instance: _T, **kwargs):
    with new_session() as session:
        session.query(model_instance).filter_by(**kwargs).delete()
        session.commit()


def generic_update(id: int, model_instance: _T, **kwargs) -> int:
    with new_session() as session:
        result = session.query(model_instance).filter_by(id=id).update(kwargs)
        session.commit()

        return result
