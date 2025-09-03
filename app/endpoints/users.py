from fastapi import APIRouter, Depends
from app.helpers.caching_proxy import cached_list_endpoint, cached_endpoint
from ..models import User
from ..jeb_schema import UserBase
from sqlalchemy import select
from ..db import get_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@cached_list_endpoint("/users", db_model=User, pydantic_model=UserBase)
async def list_users(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User))
    return result.scalars().all()


@cached_endpoint("/users/{user_id}", db_model=User, pydantic_model=UserBase)
async def read_user_by_id(user_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()


@router.get("/{user_id}/image")
async def get_user_image(user_id: int):
    return {}


@router.get("/email/{email}")
async def read_user_by_mail(email):
    return {}
