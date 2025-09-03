from fastapi import APIRouter, Depends
from app.helpers.caching_proxy import cached_list_endpoint, cached_endpoint
from ..models import Event
from ..jeb_schema import EventBase
from sqlalchemy import select
from ..db import get_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@cached_list_endpoint("/events", db_model=Event, pydantic_model=EventBase)
async def list_events(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Event))
    return result.scalars().all()


@cached_endpoint("/events/{event_id}", db_model=Event, pydantic_model=EventBase)
async def read_event(event_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Event).where(Event.id == event_id))
    return result.scalars().first()


@router.get("/{event_id}/image")
async def get_event_image(event_id: int):
    return {}
