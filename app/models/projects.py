from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship

from ..db import Base
from ._many_to_many import project_investors, user_likes
from ._table_name_provider import TableNameProvider
from .startups import Startup


class Project(Base, TableNameProvider):
    id = Column(Integer, primary_key=True, index=True)
    logo = Column(String, nullable=True)  # CDN project logo path
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    worth = Column(Integer)
    startup_id = Column(Integer, ForeignKey("startup.id"), nullable=False)

    investors = relationship(
        "Investor",
        secondary=project_investors,
        back_populates="projects",
    )
    liked_by = relationship(
        "User",
        secondary=user_likes,
        back_populates="liked_projects",
    )
