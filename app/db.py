import asyncio
from logging import getLogger

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from sqlmodel import select

logger = getLogger(__name__)

DATABASE_URL = "sqlite+aiosqlite:///app.db"

Base = declarative_base()

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_session():
    async with async_session() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    from passlib.hash import bcrypt

    from .endpoints.events import list_events
    from .endpoints.investors import list_investors
    from .endpoints.news import list_news
    from .endpoints.partners import list_partners
    from .endpoints.startups import list_startup
    from .endpoints.users import route_list_users

    async def run_task(task_func):
        async with async_session() as session:
            await task_func(session)

    await asyncio.gather(
        run_task(route_list_users),
        run_task(list_startup),
        run_task(list_events),
        run_task(list_news),
        run_task(list_partners),
        run_task(list_investors),
    )

    async with async_session() as session:
        # TODO: remove
        admin_email = "sg@a.b"
        admin_name = "sg"
        admin_password = "o"

        from .models import User

        existing_user = await session.scalar(
            select(User).where(User.email == admin_email)
        )

        if not existing_user:
            admin_user = User(
                email=admin_email,
                name=admin_name,
                authentication_string=bcrypt.hash(admin_password),
                role="ADMIN",
            )
            session.add(admin_user)
            await session.commit()
