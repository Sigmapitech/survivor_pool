from sqlalchemy import Column, ForeignKey, Integer, Table

from ..db import Base

project_investors = Table(
    "project_investors",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("project.id"), primary_key=True),
    Column("investor_id", Integer, ForeignKey("investor.id"), primary_key=True),
)

user_likes = Table(
    "user_likes",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("project.id"), primary_key=True),
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
)
