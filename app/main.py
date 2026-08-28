# main.py


from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers import patients, vaccinations

@asynccontextmanager
async def lifespan(app: FastAPI):
    # При старте создаём таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # При завершении (опционально) можно закрыть соединения

app = FastAPI(title="Vaccination Tracker", lifespan=lifespan)
app.include_router(patients.router)
app.include_router(vaccinations.router)

@app.get("/")
async def root():
    return {"message": "Vaccination Tracker API"}