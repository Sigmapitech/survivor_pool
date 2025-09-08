from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class Message(BaseModel):
    message: str


class ProjectBase(BaseModel):
    logo: str | None = None
    name: str
    descritpion: str
    worth: int
    nugget: int
