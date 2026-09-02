#crud.py

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from .models import Patient, Vaccination
from app.schemas import PatientCreate, VaccinationCreate
from datetime import date
import json
from app.redis_client import get_redis
from app.kafka_producer import get_kafka_producer
from app.config import settings


async def get_patients(db: AsyncSession, skip: int = 0, limit: int = 100):
    """Список пациентов с пагинацией"""
    result = await db.execute(select(Patient).offset(skip).limit(limit))
    return result.scalars().all()


async def get_patients_cached(db: AsyncSession, skip: int = 0, limit: int = 100):
    try:
        redis = await get_redis()
        cache_key = f"patients:skip:{skip}:limit:{limit}"
        cached = await redis.get(cache_key)
        if cached:
            return json.loads(cached)
    except Exception:
        # Если Redis недоступен, просто игнорируем кэш
        pass

    result = await get_patients(db, skip, limit)
    try:
        redis = await get_redis()
        from app.schemas import Patient
        serialized = [Patient.model_validate(p).model_dump(mode="json") for p in result]
        await redis.setex(cache_key, 60, json.dumps(serialized, default=str))
    except Exception:
        pass
    return result


async def get_patient(db: AsyncSession, patient_id: int):
    """Получить пациента по id с его вакцинациями (подгрузка связи)"""
    result = await db.execute(
        select(Patient)
        .where(Patient.id == patient_id)
        .options(selectinload(Patient.vaccinations))
    )
    return result.scalar_one_or_none()


async def create_patient(db: AsyncSession, patient: PatientCreate):
    """Создать нового пациента"""
    db_patient = Patient(
        full_name=patient.full_name,
        birth_date=patient.birth_date,
        phone=patient.phone,
        created_at=date.today(),
    )
    db.add(db_patient)
    await db.commit()
    await db.refresh(db_patient)
    return db_patient


async def create_vaccination(db: AsyncSession, vacc: VaccinationCreate):
    db_vacc = Vaccination(
        patient_id=vacc.patient_id,
        vaccine_name=vacc.vaccine_name,
        dose_number=vacc.dose_number,
        vaccination_date=vacc.vaccination_date,
        next_dose_date=vacc.next_dose_date,
    )
    db.add(db_vacc)
    await db.commit()
    await db.refresh(db_vacc)

    # Отправка события в Kafka
    try:
        producer = await get_kafka_producer()
        event = {
            "event_type": "vaccination_created",
            "vaccination_id": db_vacc.id,
            "patient_id": db_vacc.patient_id,
            "vaccine_name": db_vacc.vaccine_name,
            "dose_number": db_vacc.dose_number,
            "vaccination_date": str(db_vacc.vaccination_date),
            "next_dose_date": (
                str(db_vacc.next_dose_date) if db_vacc.next_dose_date else None
            ),
        }
        await producer.send(settings.KAFKA_TOPIC_VACCINATIONS, value=event)
    except Exception as e:
        print(f"Failed to send Kafka event: {e}")

    return db_vacc


async def get_vaccinations_by_patient(db: AsyncSession, patient_id: int):
    """Все вакцинации конкретного пациента"""
    result = await db.execute(
        select(Vaccination).where(Vaccination.patient_id == patient_id)
    )
    return result.scalars().all()
