from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession

from abstracts import BaseClient


class PostgresClient(BaseClient):
    def __init__(self, engine: AsyncEngine):
        self.engine = engine

    @asynccontextmanager
    async def get_session(self) -> AsyncSession:
        session = AsyncSession(self.engine)
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def close(self):
        await self.engine.dispose()
