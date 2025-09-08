from datetime import date

from pydantic import BaseModel, EmailStr


class StartupBase(BaseModel):
    name: str
    email: EmailStr
    legal_status: str | None = None
    address: str | None = None
    phone: str | None = None
    sector: str | None = None
    maturity: str | None = None
    created_at: date | None = None
    description: str | None = None
    website_url: str | None = None
    social_media_url: str | None = None
    project_status: str | None = None
    needs: str | None = None

    class Config:
        orm_mode = True


class StartupCreate(StartupBase):
    pass


class StartupUpdate(StartupBase):
    pass


class StartupOut(StartupBase):
    id: int
