from typing import Sequence

from ..endpoints.auth import as_enough_perms, get_user_from_token
from fastapi import HTTPException, Header, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload


from ..models import Startup
from ..schemas.startup import StartupCreate, StartupUpdate


async def create_startup(
    db: AsyncSession,
    startup_in: StartupCreate,
    authorization: str = Header(None),
) -> Startup:
    if not as_enough_perms("ADMIN", await get_user_from_token(db, authorization)):
        raise HTTPException(403, "Not enough permissions")

    new_startup = Startup(**startup_in.model_dump())
    db.add(new_startup)
    await db.commit()
    await db.refresh(new_startup)
    return new_startup


async def get_startup(db: AsyncSession, startup_id: int) -> Startup:
    result = await db.execute(
        select(Startup)
        .where(Startup.id == startup_id)
        .options(selectinload(Startup.founders))
    )
    startup = result.scalars().first()
    if not startup:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Startup not found"
        )
    return startup


async def get_startups(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> Sequence[Startup]:
    result = await db.execute(
        select(Startup)
        .offset(skip)
        .limit(limit)
        .options(selectinload(Startup.founders))
    )
    return result.scalars().all()


async def update_startup(
    db: AsyncSession,
    startup_id: int,
    startup_in: StartupUpdate,
    authorization: str = Header(None),
) -> Startup:
    if not as_enough_perms("ADMIN", await get_user_from_token(db, authorization)):
        raise HTTPException(403, "Not enough permissions")
    startup = await get_startup(db, startup_id)

    for key, value in startup_in.model_dump(exclude_unset=True).items():
        setattr(startup, key, value)
    db.add(startup)
    await db.commit()
    await db.refresh(startup)
    return startup


async def delete_startup(
    db: AsyncSession,
    startup_id: int,
    authorization: str = Header(None),
) -> None:
    if not as_enough_perms("ADMIN", await get_user_from_token(db, authorization)):
        raise HTTPException(403, "Not enough permissions")
    startup = await get_startup(db, startup_id)
    await db.delete(startup)
    await db.commit()
