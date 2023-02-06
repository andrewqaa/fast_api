from fastapi import Depends

from abstracts import BaseClient
from clients import PostgresClient
from models import User, Pet
from service import ModelService

postgres_client: PostgresClient | None = None


async def get_postgres_client() -> PostgresClient:
    return postgres_client


async def get_user_service(client: BaseClient = Depends(get_postgres_client)) -> ModelService:
    return ModelService(client, User)


async def get_pet_service(client: BaseClient = Depends(get_postgres_client)) -> ModelService:
    return ModelService(client, Pet)
