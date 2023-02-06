from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlmodel import SQLModel

from abstracts import BaseService, BaseClient


class ModelService(BaseService):
    def __init__(self, client: BaseClient, model=None):
        self.client = client
        if model:
            self.model = model

    async def insert(self, obj: SQLModel):
        async with self.client.get_session() as session:
            session.add(obj)

    async def all(self) -> list[SQLModel]:
        async with self.client.get_session() as session:
            objs = await session.execute(select(self.model).options(selectinload('*')))
            session.expunge_all()
            return objs.scalars().all()
