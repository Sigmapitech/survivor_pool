import re

from sqlalchemy import Column, Date, Integer, String, Text
from sqlalchemy.orm import relationship

from ..db import Base
from ._table_name_provider import TableNameProvider


class Startup(Base, TableNameProvider):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    legal_status = Column(String, nullable=True)
    address = Column(String, nullable=True)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    sector = Column(String, nullable=True)
    maturity = Column(String, nullable=True)
    created_at = Column(Date, nullable=True)
    description = Column(Text, nullable=True)
    website_url = Column(String, nullable=True)
    social_media_url = Column(String, nullable=True)
    project_status = Column(String, nullable=True)
    needs = Column(Text, nullable=True)

    founders = relationship(
        "Founder", back_populates="startup", cascade="all, delete-orphan"
    )
    news = relationship("News", back_populates="startup", cascade="all, delete-orphan")
