from logging import getLogger
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine

from .model import Base

logger = getLogger(__name__)

engine = create_engine("sqlite:///app.db", echo=True)


def on_startup():
    Base.metadata.create_all(bind=engine)


def get_session():
    with Session(engine) as session:
        yield session


DataBase = Annotated[Session, Depends(get_session)]
