import uvicorn

from fastapi import FastAPI, Depends
from fastapi.responses import ORJSONResponse
from sqladmin import Admin
from sqlalchemy.ext.asyncio import create_async_engine

import admin
from clients import PostgresClient
from config import settings
import dependencies
from dependencies import get_user_service, get_pet_service
from models import User, Pet, OutputUser, OutputPet
from service import ModelService


app = FastAPI(
    title="test_fast_api",
    docs_url="/swagger",
    default_response_class=ORJSONResponse,
)
engine = create_async_engine(url=f'postgresql+asyncpg://{settings.db_user}:{settings.db_pass}@{settings.db_host}:{settings.db_port}/{settings.db_name}', echo=True)


@app.on_event("startup")
async def startup():
    admin.admin = Admin(app, engine)
    dependencies.postgres_client = PostgresClient(engine)


@app.get("/users", response_model=list[OutputUser])
async def get_all_users(user_service: ModelService = Depends(get_user_service)):
    users = await user_service.all()
    return users


@app.post("/pet")
async def insert_pet(pet: Pet, pet_service: ModelService = Depends(get_pet_service)):
    await pet_service.insert(pet)


@app.get("/pets", response_model=list[OutputPet])
async def get_all_pets(pet_service: ModelService = Depends(get_pet_service)):
    pets = await pet_service.all()
    return pets


@app.post("/user")
async def insert_user(user: User, user_service: ModelService = Depends(get_user_service)):
    await user_service.insert(user)


@app.on_event("shutdown")
async def shutdown():
    try:
        await dependencies.postgres_client.close()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.backend_host,
        port=settings.backend_port,
    )
