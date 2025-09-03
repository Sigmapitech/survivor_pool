from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.helpers.caching_proxy import cached_endpoint, cached_list_endpoint

from ..db import get_session
from ..jeb_schema import InvestorBase
from ..models import Investor

router = APIRouter()


@cached_list_endpoint("/investors", db_model=Investor, pydantic_model=InvestorBase)
async def list_investors(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Investor))
    return result.scalars().all()


@cached_endpoint(
    "/investors/{investor_id}", db_model=Investor, pydantic_model=InvestorBase
)
async def read_investor(investor_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Investor).where(Investor.id == investor_id))
    return result.scalars().first()
