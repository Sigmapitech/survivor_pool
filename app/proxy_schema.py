from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class Message(BaseModel):
    message: str


class ProjectBase(BaseModel):
    logo: str | None = None
    name: str
    description: str
    worth: int
    nugget: int
    id: int
