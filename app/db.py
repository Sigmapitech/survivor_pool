from logging import getLogger
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine

from .model import SQLModel

logger = getLogger(__name__)

engine = create_engine("sqlite:///app.db", echo=True)


def on_startup():
    SQLModel.metadata.create_all(engine)
    logger.info(SQLModel.metadata.tables.keys())


def get_session():
    with Session(engine) as session:
        yield session


DataBase = Annotated[Session, Depends(get_session)]
