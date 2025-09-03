from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_session
from ..helpers.caching_proxy import cached_endpoint, cached_list_endpoint
from ..jeb_schema import PartnerBase
from ..models import Partner

router = APIRouter()


@cached_list_endpoint("/partners", db_model=Partner, pydantic_model=PartnerBase)
async def list_partners(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Partner))
    return result.scalars().all()


@cached_endpoint("/partners/{partner_id}", db_model=Partner, pydantic_model=PartnerBase)
async def read_partners(partner_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Partner).where(Partner.id == partner_id))
    return result.scalars().first()
