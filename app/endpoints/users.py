from fastapi import APIRouter, Depends, HTTPException
from passlib.hash import bcrypt
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_session
from ..helpers.caching_proxy import cached_endpoint, cached_list_endpoint, get_image
from ..jeb_schema import UserBase
from ..models import User
from ..proxy_schema import Message
from .auth import PasswordStr

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


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar()
    if user is None:
        raise HTTPException(404, "User not found")
    await db.delete(user)
    await db.commit()
    return Message(message="User deleted sucessfuly")


class UpdateRequest(BaseModel):
    email: EmailStr
    password: PasswordStr
    name: str
    role: str


class PatchRequest(BaseModel):
    email: EmailStr | None = None
    password: PasswordStr | None = None
    name: str | None = None
    role: str | None = None


@router.put("/{user_id}")
async def update_user(
    user_id: int, data: UpdateRequest, db: AsyncSession = Depends(get_session)
) -> UserBase:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar()
    if user is None:
        raise HTTPException(404, "User not found")
    setattr(user, "email", data.email)
    setattr(user, "auth", bcrypt.hash(data.password))
    setattr(user, "name", data.name)
    setattr(user, "role", data.role)
    await db.commit()
    await db.refresh(user)
    return UserBase.model_validate(user, from_attributes=True)


@router.patch("/{user_id}")
async def patch_user(
    user_id: int, data: PatchRequest, db: AsyncSession = Depends(get_session)
) -> UserBase:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar()
    if user is None:
        raise HTTPException(404, "User not found")
    if data.email:
        setattr(user, "email", data.email)
    if data.password:
        setattr(user, "auth", bcrypt.hash(data.password))
    if data.name:
        setattr(user, "name", data.name)
    if data.role:
        setattr(user, "role", data.role)
    await db.commit()
    await db.refresh(user)
    return UserBase.model_validate(user, from_attributes=True)
