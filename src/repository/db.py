# For simplicity's sake, we don´t do migrations
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src import config
from .model._base import Base  # noqa


db = create_engine(config.DB_NAME, connect_args={"check_same_thread": False})
db.echo = config.DB_ECHO
Base.metadata.create_all(db)  # to be replaced by alembic migrations
Session = sessionmaker(bind=db, autoflush=False, autocommit=False)


@contextmanager
def new_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()
