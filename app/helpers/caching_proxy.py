from sqlalchemy import select

from ..config import settings
from ..models import Startup

import aiohttp
from fastapi import Depends, APIRouter
from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession
from http import HTTPStatus

from app.db import get_session


router = APIRouter()


async def fetch_from_api(api_url: str, **kwargs):
    url = (settings.jeb_api_url + api_url).format(**kwargs)
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url, headers={"X-Group-Authorization": settings.jeb_api_auth}
        ) as response:
            return await response.json(), response.status


def cached_endpoint(api_url: str, db_model, pydantic_model):
    def decorator(func):
        @wraps(func)
        async def wrapper(db: AsyncSession = Depends(get_session), **kwargs):
            result = await db.execute(select(db_model))
            collected = result.scalars().all()

            if collected is not None:
                return [
                    pydantic_model.model_validate(s, from_attributes=True)
                    for s in collected
                ]

            res, status = await fetch_from_api(api_url, **kwargs)

            if status != HTTPStatus.OK.value:
                return res

            items = []
            for item in res:
                model_instance = pydantic_model(**item)
                items.append(model_instance)
                db.add(db_model(**model_instance.model_dump()))

            await db.commit()
            return items

        return router.get("/api" + api_url)(wrapper)

    return decorator
