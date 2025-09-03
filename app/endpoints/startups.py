from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_session
from ..helpers.caching_proxy import cached_endpoint, cached_list_endpoint, get_image
from ..jeb_schema import StartupBase
from ..models import Startup

router = APIRouter()


@cached_list_endpoint("/startups", db_model=Startup, pydantic_model=StartupBase)
async def list_startup(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Startup))
    return result.scalars().all()


@cached_endpoint("/startups/{startup_id}", db_model=Startup, pydantic_model=StartupBase)
async def read_startup(startup_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Startup).where(Startup.id == startup_id))
    return result.scalars().first()


@get_image("/startups/{startup_id}/founders/{founder_id}/image")
async def get_founder_of_startup_image(
    startup_id: int, founder_id: int
): ...  # The decorator does all so no need to complete this
