from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from db.models import Base

engine = create_async_engine("sqlite+aiosqlite:///db/lyceum.db", echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
