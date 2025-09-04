import hashlib
import logging
import os
from functools import wraps
from http import HTTPStatus
from pathlib import Path

import aiohttp
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import settings
from ..db import get_session

router = APIRouter()
logger = logging.getLogger(__name__)

CACHE_DIR = Path("app/static/images")
os.makedirs(CACHE_DIR, exist_ok=True)


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
            filepath = CACHE_DIR / (
                f"{hashlib.sha256(api_url.format(**kwargs).encode()).hexdigest()}.png"
            )
            if filepath.exists():
                return FileResponse(filepath)
            res, status = await fetch_from_api(api_url, **kwargs)
            if status != HTTPStatus.OK.value:
                raise HTTPException(status, detail=res)
            with open(filepath, "wb") as f:
                if isinstance(res, bytes):
                    f.write(res)
                else:
                    raise ValueError(
                        "Expected 'res' to be of type 'bytes' for writing to file."
                    )

            return FileResponse(filepath)

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
