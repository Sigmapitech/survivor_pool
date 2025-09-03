from fastapi import APIRouter, Depends
from app.helpers.caching_proxy import cached_list_endpoint, cached_endpoint
from ..models import News
from ..jeb_schema import NewsBase
from sqlalchemy import select
from ..db import get_session
from sqlalchemy.ext.asyncio import AsyncSession

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
