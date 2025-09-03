from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.helpers.caching_proxy import cached_endpoint, cached_list_endpoint

from ..db import get_session
from ..jeb_schema import NewsBase
from ..models import News

router = APIRouter()


@cached_list_endpoint("/news", db_model=News, pydantic_model=NewsBase)
async def list_news(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(News))
    return result.scalars().all()


@cached_endpoint("/news/{news_id}", db_model=News, pydantic_model=NewsBase)
async def read_news(news_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(News).where(News.id == news_id))
    return result.scalars().first()


@router.get("/{news_id}/image")
async def get_news_image(news_id: int):
    return {}
