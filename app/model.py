import logging
import re
from datetime import datetime

from sqlalchemy import event
from sqlmodel import Field, SQLModel

logger = logging.getLogger(__package__)


class BaseTable(SQLModel):
    id: int = Field(primary_key=True, index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def __init_subclass__(cls, **kwargs):

        event.listen(cls, "before_update", cls._update_timestamp)
        cls.__tablename__ = re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()
        super().__init_subclass__(**kwargs)

    @staticmethod
    def _update_timestamp(mapper, connection, target):
        target.updated_at = datetime.now()
