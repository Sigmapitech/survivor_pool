from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_session
from ..helpers.caching_proxy import cached_endpoint, cached_list_endpoint, get_image
from ..jeb_schema import UserBase
from ..models import User

router = APIRouter()


@cached_list_endpoint("/users", db_model=User, pydantic_model=UserBase)
async def list_users(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User))
    return result.scalars().all()


@cached_endpoint("/users/{user_id}", db_model=User, pydantic_model=UserBase)
async def read_user_by_id(user_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()


@get_image("/users/{user_id}/image")
async def get_user_image(
    user_id: int,
): ...  # The decorator does all so no need to complete this


@cached_endpoint("/users/email/{email}", db_model=User, pydantic_model=UserBase)
async def read_user_by_mail(email, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()
