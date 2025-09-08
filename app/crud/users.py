from typing import Sequence

from fastapi import HTTPException, status
from passlib.hash import bcrypt
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..models import User
from ..schemas.users import PatchRequest, UpdateRequest


async def create_user(db: AsyncSession, user_in: UpdateRequest) -> User:
    data = user_in.model_dump()

    if "password" in data:
        data["auth"] = bcrypt.hash(data.pop("password"))

    if "email" in data and data["email"]:
        data["email"] = str(data["email"])

    new_user = User(**data)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_user(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        return None
    return user


async def get_user_by_email(db: AsyncSession, user_email: EmailStr) -> User | None:
    result = await db.execute(select(User).where(User.email == user_email))
    return result.scalars().first()


async def get_users(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> Sequence[User]:
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


async def update_user(db: AsyncSession, user_id: int, user_in: UpdateRequest) -> User:
    user = await get_user(db, user_id)
    data = user_in.model_dump()

    for key, value in data.items():
        if key == "password" and value:
            setattr(user, "auth", bcrypt.hash(value))
        elif key == "email" and value:
            setattr(user, "email", str(value))
        elif value is not None:
            setattr(user, key, value)

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def patch_user(db: AsyncSession, user_id: int, user_in: PatchRequest) -> User:
    user = await get_user(db, user_id)
    data = user_in.model_dump(exclude_unset=True)

    for key, value in data.items():
        if key == "password" and value:
            setattr(user, "auth", bcrypt.hash(value))
        elif key == "email" and value:
            setattr(user, "email", str(value))
        elif value is not None:
            setattr(user, key, value)

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user_id: int) -> None:
    user = await get_user(db, user_id)
    await db.delete(user)
    await db.commit()
