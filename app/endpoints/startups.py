from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.jeb_schema import StartupBase

from ..models import Startup
from ..helpers.caching_proxy import cached_endpoint, cached_list_endpoint

router = APIRouter()


@cached_list_endpoint("/startups", db_model=Startup, pydantic_model=StartupBase)
async def list_startup(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Startup))
    return result.scalars().all()


@cached_endpoint("/startups/{startup_id}", db_model=Startup, pydantic_model=StartupBase)
async def read_startup(startup_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Startup).where(Startup.id == startup_id))
    return result.scalars().first()


@router.get("/{startup_id}/founders/{founder_id}/image")
async def read_founder_image(startup_id: int, founder_id: int):
    return {}
