from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class Message(BaseModel):
    message: str
