from ..config import settings

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
            print("@" * 999)
            print(response.json())
            return await response.json(), response.status


def cached_endpoint_inner(api_url: str, convert_in, convert_out):
    def decorator(func):
        @wraps(func)
        async def wrapper(db: AsyncSession = Depends(get_session), **kwargs):
            collected = await func(**kwargs, db=db)

            if collected:
                return convert_out(collected)

            res, status = await fetch_from_api(api_url, **kwargs)

            if status != HTTPStatus.OK.value:
                return res

            items = convert_in(db, res)
            await db.commit()
            return items

        return router.get("/api" + api_url)(wrapper)

    return decorator


def cached_list_endpoint(api_url: str, db_model, pydantic_model):
    def convert_in(db, res):
        items = []
        for item in res:
            model_instance = pydantic_model(**item)
            items.append(model_instance)

            db.add(db_model(**model_instance.model_dump()))

        return items

    def convert_out(collected):
        return [
            pydantic_model.model_validate(s, from_attributes=True) for s in collected
        ]

    return cached_endpoint_inner(api_url, convert_in, convert_out)


def cached_endpoint(api_url: str, db_model, pydantic_model):
    def convert_in(db, res):
        model_instance = pydantic_model(**res)
        db.add(db_model(**model_instance.model_dump()))
        return model_instance

    def convert_out(collected):
        return pydantic_model.model_validate(collected, from_attributes=True)

    return cached_endpoint_inner(api_url, convert_in, convert_out)
