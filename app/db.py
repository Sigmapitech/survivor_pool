from logging import getLogger

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .models import Base

logger = getLogger(__name__)

DATABASE_URL = "sqlite+aiosqlite:///app.db"

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

    from .endpoints.events import list_events
    from .endpoints.investors import list_investors
    from .endpoints.news import list_news
    from .endpoints.partners import list_partners
    from .endpoints.startups import list_startup
    from .endpoints.users import list_users

    async with async_session() as session:
        await list_users(session)
        await list_startup(session)
        await list_events(session)
        await list_news(session)
        await list_partners(session)
        await list_investors(session)
