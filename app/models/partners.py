from sqlalchemy import Column, Date, Integer, String, Text

from ..db import Base
from ._table_name_provider import TableNameProvider


class Partner(Base, TableNameProvider):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    legal_status = Column(String, nullable=True)
    address = Column(String, nullable=True)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    created_at = Column(Date, nullable=True)
    description = Column(Text, nullable=False)
    partnership_type = Column(String, nullable=False)
