import aiohttp
from fastapi import APIRouter

from ..config import settings

router = APIRouter()


@router.get("/")
async def list_startup():
    async with aiohttp.ClientSession() as session:
        headers = {"X-Group-Authorization": settings.jeb_api_auth}

        async with session.get(
            "https://api.jeb-incubator.com/startups", headers=headers
        ) as response:
            res = await response.json()

            return res


@router.get("/{startup_id}")
async def read_startup(startup_id: int):
    return {}


@router.get("/{startup_id}/founders/{founder_id}/image")
async def read_founder_image(startup_id: int, founder_id: int):
    return {}
