from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import date
import json
from typing import List, Optional

from app.models import Patient, Vaccination
from app.schemas import PatientCreate, VaccinationCreate
from app.redis_client import get_redis
from app.kafka_producer import get_kafka_producer
from app.config import settings


# ===== PATIENT CRUD =====

async def get_patient(db: AsyncSession, patient_id: int) -> Optional[Patient]:
    """Получить пациента по ID с загрузкой всех вакцинаций"""
    result = await db.execute(
        select(Patient)
        .options(selectinload(Patient.vaccinations))
        .where(Patient.id == patient_id)
    )
    return result.scalar_one_or_none()


async def get_patients(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 100
) -> List[Patient]:
    """Получить список пациентов с пагинацией"""
    result = await db.execute(
        select(Patient)
        .offset(skip)
        .limit(limit)
        .order_by(Patient.id)
    )
    return result.scalars().all()


async def get_patients_cached(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 100
) -> List[Patient]:
    """Получить список пациентов с кэшированием в Redis"""
    # Пытаемся получить из кэша
    try:
        redis = await get_redis()
        cache_key = f"patients:skip:{skip}:limit:{limit}"
        cached = await redis.get(cache_key)
        
        if cached:
            # Возвращаем из кэша
            data = json.loads(cached)
            # Преобразуем обратно в объекты Patient
            from app.schemas import Patient as PatientSchema
            return [PatientSchema(**item) for item in data]
    except Exception as e:
        print(f"Redis get error: {e}")
    
    # Получаем из БД
    patients = await get_patients(db, skip, limit)
    
    # Сохраняем в кэш
    try:
        redis = await get_redis()
        cache_key = f"patients:skip:{skip}:limit:{limit}"
        
        # Сериализуем объекты SQLAlchemy
        from app.schemas import Patient as PatientSchema
        serialized = [
            PatientSchema.model_validate(p).model_dump(mode="json") 
            for p in patients
        ]
        
        await redis.set(cache_key, json.dumps(serialized, default=str), ex=60)
        
    except Exception as e:
        print(f"Redis set error: {e}")
    
    return patients


async def create_patient(db: AsyncSession, patient: PatientCreate) -> Patient:
    """Создать нового пациента"""
    db_patient = Patient(
        full_name=patient.full_name,
        birth_date=patient.birth_date,
        phone=patient.phone
    )
    db.add(db_patient)
    await db.commit()
    await db.refresh(db_patient)
    
    # Инвалидируем кэш
    try:
        redis = await get_redis()
        # Очищаем все кэшированные списки пациентов
        keys = await redis.keys("patients:*")
        if keys:
            await redis.delete(*keys)
    except Exception as e:
        print(f"Redis invalidation error: {e}")
    
    return db_patient


# ===== VACCINATION CRUD =====

async def get_vaccination(
    db: AsyncSession, 
    vaccination_id: int
) -> Optional[Vaccination]:
    """Получить вакцинацию по ID"""
    result = await db.execute(
        select(Vaccination).where(Vaccination.id == vaccination_id)
    )
    return result.scalar_one_or_none()


async def get_vaccinations_by_patient(
    db: AsyncSession, 
    patient_id: int
) -> List[Vaccination]:
    """Получить все вакцинации пациента"""
    result = await db.execute(
        select(Vaccination)
        .where(Vaccination.patient_id == patient_id)
        .order_by(Vaccination.vaccination_date.desc())
    )
    return result.scalars().all()


async def get_all_vaccinations(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 100
) -> List[Vaccination]:
    """Получить все вакцинации с пагинацией"""
    result = await db.execute(
        select(Vaccination)
        .offset(skip)
        .limit(limit)
        .order_by(Vaccination.id)
    )
    return result.scalars().all()


async def create_vaccination(
    db: AsyncSession, 
    vacc: VaccinationCreate
) -> Vaccination:
    """Создать новую вакцинацию и отправить событие в Kafka"""
    # Создаем запись
    db_vacc = Vaccination(
        patient_id=vacc.patient_id,
        vaccine_name=vacc.vaccine_name,
        dose_number=vacc.dose_number,
        vaccination_date=vacc.vaccination_date,
        next_dose_date=vacc.next_dose_date
    )
    db.add(db_vacc)
    await db.commit()
    await db.refresh(db_vacc)
    
    # Отправляем событие в Kafka
    try:
        producer = await get_kafka_producer()
        event = {
            "event_type": "vaccination_created",
            "vaccination_id": db_vacc.id,
            "patient_id": db_vacc.patient_id,
            "vaccine_name": db_vacc.vaccine_name,
            "dose_number": db_vacc.dose_number,
            "vaccination_date": db_vacc.vaccination_date.isoformat(),
            "next_dose_date": db_vacc.next_dose_date.isoformat() if db_vacc.next_dose_date else None,
            "timestamp": date.today().isoformat()
        }
        
        await producer.send(
            settings.KAFKA_TOPIC_VACCINATIONS, 
            value=event
        )
        print(f"Kafka event sent: {event}")
        
    except Exception as e:
        print(f"Failed to send Kafka event: {e}")
        # Не блокируем создание вакцинации, если Kafka недоступна
    
    return db_vacc


async def update_vaccination(
    db: AsyncSession, 
    vaccination_id: int, 
    vacc_update: VaccinationCreate
) -> Optional[Vaccination]:
    """Обновить существующую вакцинацию"""
    db_vacc = await get_vaccination(db, vaccination_id)
    if not db_vacc:
        return None
    
    # Обновляем поля
    db_vacc.patient_id = vacc_update.patient_id
    db_vacc.vaccine_name = vacc_update.vaccine_name
    db_vacc.dose_number = vacc_update.dose_number
    db_vacc.vaccination_date = vacc_update.vaccination_date
    db_vacc.next_dose_date = vacc_update.next_dose_date
    
    await db.commit()
    await db.refresh(db_vacc)
    return db_vacc


async def delete_vaccination(
    db: AsyncSession, 
    vaccination_id: int
) -> bool:
    """Удалить вакцинацию"""
    db_vacc = await get_vaccination(db, vaccination_id)
    if not db_vacc:
        return False
    
    await db.delete(db_vacc)
    await db.commit()
    return True