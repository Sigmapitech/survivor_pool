from typing import Sequence

from fastapi import Header, HTTPException
from passlib.hash import bcrypt
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..endpoints.auth import get_user_from_token
from ..models import User
from ..schemas.users import PatchRequest, UpdateRequest


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


async def update_user(
    db: AsyncSession,
    user_id: int,
    user_in: UpdateRequest,
    authorization: str = Header(None),
) -> User:
    requester = get_user_from_token(db, authorization)
    user = await get_user(db, user_id)
    if requester != user:
        raise HTTPException(403, "You are not the user")

    if getattr(user, "email") != user_in.email:
        result = await db.execute(select(User).filter(User.email == user_in.email))
        collected = result.scalars().all()
        if len(collected) > 0:
            raise HTTPException(status_code=400, detail="Email already used")

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


async def patch_user(
    db: AsyncSession,
    user_id: int,
    user_in: PatchRequest,
    authorization: str = Header(None),
) -> User:
    requester = get_user_from_token(db, authorization)
    user = await get_user(db, user_id)
    if requester != user:
        raise HTTPException(403, "You are not the user")
    if user_in.email and getattr(user, "email") != user_in.email:
        result = await db.execute(select(User).filter(User.email == user_in.email))
        collected = result.scalars().all()
        if len(collected) > 0:
            raise HTTPException(status_code=400, detail="Email already used")

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


async def delete_user(
    db: AsyncSession,
    user_id: int,
    authorization: str = Header(None),
) -> None:
    requester = get_user_from_token(db, authorization)
    user = await get_user(db, user_id)
    if requester != user:
        raise HTTPException(403, "You are not the user")
    await db.delete(user)
    await db.commit()
