from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class EventBase(BaseModel):
    id: int
    name: str
    dates: str | None
    location: str | None
    description: str | None
    event_type: str | None
    target_audience: str | None


class Founder(BaseModel):
    id: int
    name: str
    startup_id: int


class InvestorBase(BaseModel):
    id: int
    name: str
    legal_status: str | None
    address: str | None
    email: str
    phone: str | None
    created_at: date | None
    description: str | None
    investor_type: str | None
    investment_focus: str | None


class NewsBase(BaseModel):
    id: int
    news_date: date | None
    location: str | None
    title: str | None
    category: str | None
    startup_id: int | None


class NewsDetail(NewsBase):
    description: str


class PartnerBase(BaseModel):
    id: int
    name: str | None
    legal_status: str | None
    address: str | None
    email: str
    phone: str | None
    created_at: date | None
    description: str
    partnership_type: str


class StartupBase(BaseModel):
    id: int
    name: str
    legal_status: str | None
    address: str | None
    email: str
    phone: str | None
    sector: str | None
    maturity: str | None


class StartupDetail(StartupBase):
    created_at: date | None
    description: str | None
    website_url: str | None
    social_media_url: str | None
    project_status: str | None
    needs: str | None
    founders: List[Founder]


class UserBase(BaseModel):
    id: int
    email: str
    name: str
    role: str
    founder_id: int | None
    investor_id: int | None


class HTTPValidationErrorBase(BaseModel):
    log: list[int | str]
    msg: str
    type: str
