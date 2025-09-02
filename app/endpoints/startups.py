import aiohttp
from fastapi import APIRouter, Depends
from sqlalchemy import select

from app.db import get_session
from app.jeb_schema import StartupBase

from ..config import settings
from ..models import Startup

router = APIRouter()


@router.get("/")
async def list_startup(db=Depends(get_session)):
    result = db.execute(select(Startup))
    collected = result.scalars().all()

    if len(collected) > 0:
        return [StartupBase.model_validate(s, from_attributes=True) for s in collected]

    startups = []

    async with aiohttp.ClientSession() as session:
        headers = {"X-Group-Authorization": settings.jeb_api_auth}

        async with session.get(
            "https://api.jeb-incubator.com/startups", headers=headers
        ) as response:
            res = await response.json()

        for item in res:
            startup = StartupBase(**item)
            startups.append(startup)

            db.add(Startup(**startup.model_dump()))

    db.commit()
    return startups


@router.get("/{startup_id}")
async def read_startup(startup_id: int):
    return {}


@router.get("/{startup_id}/founders/{founder_id}/image")
async def read_founder_image(startup_id: int, founder_id: int):
    return {}
