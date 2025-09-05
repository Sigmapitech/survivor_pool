from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from ..db import Base
from ._table_name_provider import TableNameProvider


class News(Base, TableNameProvider):
    id = Column(Integer, primary_key=True, index=True)
    news_date = Column(Date, nullable=True)
    location = Column(String, nullable=True)
    title = Column(String, nullable=True)
    category = Column(String, nullable=True)
    startup_id = Column(Integer, ForeignKey("startup.id"), nullable=True)
    description = Column(Text, nullable=True)
    startup = relationship("Startup", back_populates="news")
