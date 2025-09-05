from sqlalchemy import Column, Integer, String, Text

from ..db import Base
from ._table_name_provider import TableNameProvider


class Event(Base, TableNameProvider):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    dates = Column(String, nullable=True)
    location = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    event_type = Column(String, nullable=True)
    target_audience = Column(String, nullable=True)
