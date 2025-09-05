from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..db import Base
from ._table_name_provider import TableNameProvider


class Founder(Base, TableNameProvider):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    startup_id = Column(Integer, ForeignKey("startup.id"), nullable=False)
    startup = relationship("Startup", back_populates="founders")
