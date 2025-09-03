from fastapi import APIRouter, Depends
from app.helpers.caching_proxy import cached_list_endpoint, cached_endpoint
from ..models import Partner
from ..jeb_schema import PartnerBase
from sqlalchemy import select
from ..db import get_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@cached_list_endpoint("/partners", db_model=Partner, pydantic_model=PartnerBase)
async def list_partners(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Partner))
    return result.scalars().all()


@cached_endpoint("/partners/{partner_id}", db_model=Partner, pydantic_model=PartnerBase)
async def read_partners(partner_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Partner).where(Partner.id == partner_id))
    return result.scalars().first()
