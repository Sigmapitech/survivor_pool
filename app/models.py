import logging
import re

from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship

logger = logging.getLogger(__package__)


Base = declarative_base()


class TableNameProvider:
    id = Column(Integer, primary_key=True, index=True)

    def __init_subclass__(cls, **kwargs):
        cls.__tablename__ = re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()
        super().__init_subclass__(**kwargs)


class Event(Base, TableNameProvider):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    dates = Column(String, nullable=True)
    location = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    event_type = Column(String, nullable=True)
    target_audience = Column(String, nullable=True)


class Founder(Base, TableNameProvider):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    startup_id = Column(Integer, ForeignKey("startup.id"), nullable=False)
    startup = relationship("Startup", back_populates="founders")


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


class News(Base, TableNameProvider):
    id = Column(Integer, primary_key=True, index=True)
    news_date = Column(Date, nullable=True)
    location = Column(String, nullable=True)
    title = Column(String, nullable=True)
    category = Column(String, nullable=True)
    startup_id = Column(Integer, ForeignKey("startup.id"), nullable=True)
    description = Column(Text, nullable=True)
    startup = relationship("Startup", back_populates="news")


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


class User(Base, TableNameProvider):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    founder_id = Column(Integer, ForeignKey("founder.id"), nullable=True)
    investor_id = Column(Integer, ForeignKey("investor.id"), nullable=True)


class HTTPValidationError(Base, TableNameProvider):
    id = Column(Integer, primary_key=True, index=True)
    log = Column(Text, nullable=False)
    msg = Column(String, nullable=False)
    type = Column(String, nullable=False)
