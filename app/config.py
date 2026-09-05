# config.py

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@postgres:5432/vaccination",
    )
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv(
        "KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"
    )
    KAFKA_TOPIC_VACCINATIONS: str = os.getenv(
        "KAFKA_TOPIC_VACCINATIONS", "vaccination_events"
    )


settings = Settings()
