from typing import List

from fastapi import APIRouter, Depends, Header, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud_startup
from ..db import get_session
from ..helpers.caching_proxy import cached_endpoint, cached_list_endpoint, get_image
from ..jeb_schema import StartupBase
from ..models import Startup
from ..proxy_schema import Message
from ..schemas.startup import StartupCreate, StartupOut, StartupUpdate

router = APIRouter(tags=["startups"])


@cached_list_endpoint("/startups", db_model=Startup, pydantic_model=StartupBase)
async def list_startup(db: AsyncSession = Depends(get_session), skip=0, limit=50):
    return await crud_startup.get_startups(db, skip, limit)


@cached_endpoint("/startups/{startup_id}", db_model=Startup, pydantic_model=StartupBase)
async def read_startup(startup_id: int, db: AsyncSession = Depends(get_session)):
    return await crud_startup.get_startup(db, startup_id)


@get_image("/startups/{startup_id}/founders/{founder_id}/image")
async def get_founder_of_startup_image(
    startup_id: int, founder_id: int
): ...  # The decorator does all so no need to complete this


@router.post(
    "/",
    response_model=StartupOut,
    status_code=status.HTTP_201_CREATED,
    description="Create a new startup",
    responses={
        201: {"model": StartupOut, "description": "Startup created"},
        400: {"model": Message, "description": "Invalid input"},
    },
)
async def create_startup(
    startup: StartupCreate,
    db: AsyncSession = Depends(get_session),
    authorization: str = Header(None),
):
    return await crud_startup.create_startup(db, startup, authorization)


@router.put(
    "/{startup_id}",
    response_model=StartupOut,
    description="Update a startup",
    responses={
        404: {"model": Message, "description": "Startup not found"},
        200: {"model": StartupOut, "description": "Startup updated"},
    },
)
async def update_startup(
    startup_id: int,
    startup: StartupUpdate,
    db: AsyncSession = Depends(get_session),
    authorization: str = Header(None),
):
    return await crud_startup.update_startup(db, startup_id, startup, authorization)


@router.patch(
    "/{startup_id}",
    response_model=StartupOut,
    description="Patch a startup",
    responses={
        404: {"model": Message, "description": "Startup not found"},
        200: {"model": StartupOut, "description": "Startup patched"},
    },
)
async def patch_startup(
    startup_id: int,
    startup: StartupUpdate,
    db: AsyncSession = Depends(get_session),
    authorization: str = Header(None),
):
    return await crud_startup.update_startup(db, startup_id, startup, authorization)


@router.delete(
    "/{startup_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete a startup",
    responses={
        404: {"model": Message, "description": "Startup not found"},
    },
)
async def delete_startup(
    startup_id: int,
    db: AsyncSession = Depends(get_session),
    authorization: str = Header(None),
):
    await crud_startup.delete_startup(db, startup_id, authorization)
