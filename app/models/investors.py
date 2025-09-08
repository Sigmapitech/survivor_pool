from sqlalchemy import Column, Date, Integer, String, Text
from sqlalchemy.orm import relationship

from ..db import Base
from ._many_to_many import project_investors
from ._table_name_provider import TableNameProvider


class Investor(Base, TableNameProvider):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    legal_status = Column(String, nullable=True)
    address = Column(String, nullable=True)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    created_at = Column(Date, nullable=True)
    description = Column(Text, nullable=True)
    investor_type = Column(String, nullable=True)
    investment_focus = Column(String, nullable=True)

    projects = relationship(
        "Project",
        secondary=project_investors,
        back_populates="investors",
    )
