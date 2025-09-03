import logging
from functools import wraps
from http import HTTPStatus

import aiohttp
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session

from ..config import settings

router = APIRouter()
logger = logging.getLogger(__name__)


async def fetch_from_api(api_url: str, **kwargs):
    url = (settings.jeb_api_url + api_url).format(**kwargs)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url, headers={"X-Group-Authorization": settings.jeb_api_auth}
            ) as response:
                logger.debug("@" * 999)
                match response.content_type:
                    case "application/json":
                        logger.debug(await response.json())
                        return await response.json(), response.status
                    case "image/png":
                        data = await response.read()
                        return data, response.status
                    case _:
                        return (None, 500)

    except Exception as e:
        logger.error(e)
        return ({"detail": f"External api call fail: {e}"}, 404)


def get_image(api_url: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(**kwargs):
            res, status = await fetch_from_api(api_url, **kwargs)
            if status != HTTPStatus.OK.value:
                raise HTTPException(status, detail=res)
            return Response(content=res, media_type="image/png")

        return router.get("/api" + api_url)(wrapper)

    return decorator


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
