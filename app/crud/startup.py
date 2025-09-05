from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status

from ..models import Startup
from ..schemas.startup import StartupCreate, StartupUpdate


async def create_startup(db: AsyncSession, startup_in: StartupCreate) -> Startup:
    new_startup = Startup(**startup_in.dict())
    db.add(new_startup)
    await db.commit()
    await db.refresh(new_startup)
    return new_startup


async def get_startup(db: AsyncSession, startup_id: int) -> Startup:
    result = await db.execute(select(Startup).where(Startup.id == startup_id))
    startup = result.scalars().first()
    if not startup:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Startup not found"
        )
    return startup


async def get_startups(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> Sequence[Startup]:
    result = await db.execute(select(Startup).offset(skip).limit(limit))
    return result.scalars().all()


async def update_startup(
    db: AsyncSession, startup_id: int, startup_in: StartupUpdate
) -> Startup:
    startup = await get_startup(db, startup_id)

    for key, value in startup_in.model_dump(exclude_unset=True).items():
        setattr(startup, key, value)
    db.add(startup)
    await db.commit()
    await db.refresh(startup)
    return startup


async def delete_startup(db: AsyncSession, startup_id: int) -> None:
    startup = await get_startup(db, startup_id)
    await db.delete(startup)
    await db.commit()
