import logging
import re

from sqlmodel import Field, SQLModel

logger = logging.getLogger(__package__)


class BaseTable(SQLModel):
    id: int = Field(primary_key=True, index=True)

    def __init_subclass__(cls, **kwargs):
        cls.__tablename__ = re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()
        super().__init_subclass__(**kwargs)
