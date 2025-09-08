import re
from typing import Annotated

from pydantic import BaseModel, EmailStr, StringConstraints

PasswordStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=8,
        max_length=50,
        pattern=re.compile(
            r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        ),
    ),
]


class UpdateRequest(BaseModel):
    email: EmailStr
    password: PasswordStr
    name: str
    role: str


class PatchRequest(BaseModel):
    email: EmailStr | None = None
    password: PasswordStr | None = None
    name: str | None = None
    role: str | None = None
