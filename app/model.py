import logging
import re

from sqlalchemy import Column, Date, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship

logger = logging.getLogger(__package__)


Base = declarative_base()


class TableNameProvider:
    id = Column(Integer, primary_key=True, index=True)

    def __init_subclass__(cls, **kwargs):
        cls.__tablename__ = re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()
        super().__init_subclass__(**kwargs)


class Startup(Base, TableNameProvider):
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

    # TODO: founders, news
