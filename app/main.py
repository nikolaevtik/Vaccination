# main.py


from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers import patients, vaccinations
from app.kafka_producer import get_kafka_producer, shutdown_kafka_producer


@asynccontextmanager
async def lifespan(app: FastAPI):
    # При старте
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Инициализация Kafka (опционально)
    try:
        await get_kafka_producer()
        print("Kafka producer initialized")
    except Exception as e:
        print(f"Kafka not available: {e}")
    yield
    # При завершении
    await shutdown_kafka_producer()

app = FastAPI(title="Vaccination Tracker", lifespan=lifespan)
app.include_router(patients.router)
app.include_router(vaccinations.router)

@app.get("/")
async def root():
    return {"message": "Vaccination Tracker API"}