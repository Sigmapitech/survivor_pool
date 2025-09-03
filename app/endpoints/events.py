from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_session
from ..helpers.caching_proxy import cached_endpoint, cached_list_endpoint, get_image
from ..jeb_schema import EventBase
from ..models import Event

router = APIRouter()


@cached_list_endpoint("/events", db_model=Event, pydantic_model=EventBase)
async def list_events(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Event))
    return result.scalars().all()


@cached_endpoint("/events/{event_id}", db_model=Event, pydantic_model=EventBase)
async def read_event(event_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Event).where(Event.id == event_id))
    return result.scalars().first()


@get_image("/events/{event_id}/image")
async def get_event_image(
    event_id: int,
): ...  # The decorator does all so no need to complete this
