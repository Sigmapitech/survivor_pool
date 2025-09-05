from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.startup import StartupCreate, StartupOut, StartupUpdate

from ..db import get_session
from ..helpers.caching_proxy import cached_endpoint, cached_list_endpoint, get_image
from ..jeb_schema import StartupBase
from ..models import Startup

from app import crud_startup

router = APIRouter(tags=["startups"])


@cached_list_endpoint("/startups", db_model=Startup, pydantic_model=StartupBase)
async def list_startup(db: AsyncSession = Depends(get_session), skip=0, limit=50):
    result = await db.execute(select(Startup))
    return await crud_startup.get_startups(db, skip, limit)


@cached_endpoint("/startups/{startup_id}", db_model=Startup, pydantic_model=StartupBase)
async def read_startup(startup_id: int, db: AsyncSession = Depends(get_session)):
    return await crud_startup.get_startup(db, startup_id)


@get_image("/startups/{startup_id}/founders/{founder_id}/image")
async def get_founder_of_startup_image(
    startup_id: int, founder_id: int
): ...  # The decorator does all so no need to complete this


@router.post("/", response_model=StartupOut)
async def create_startup(
    startup: StartupCreate, db: AsyncSession = Depends(get_session)
):
    return await crud_startup.create_startup(db, startup)


@router.put("/{startup_id}", response_model=StartupOut)
async def update_startup(
    startup_id: int, startup: StartupUpdate, db: AsyncSession = Depends(get_session)
):
    return await crud_startup.update_startup(db, startup_id, startup)


@router.delete("/{startup_id}", status_code=204)
async def delete_startup(startup_id: int, db: AsyncSession = Depends(get_session)):
    await crud_startup.delete_startup(db, startup_id)
