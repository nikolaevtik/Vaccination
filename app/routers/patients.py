# routers/patients.py

from urllib import response

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app import crud, schemas
from app.crud import get_patients_cached

router = APIRouter(prefix="/patients", tags=["patients"])


@router.get("/", response_model=list[schemas.Patient])
async def read_patients(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await get_patients_cached(db, skip, limit)


@router.post("/", response_model=schemas.PatientRead)  # не list, а одна запись
async def create_patient(
    patient: schemas.PatientCreate, db: AsyncSession = Depends(get_db)  # тело запроса
):
    """Добавление нового пациента"""
    return await crud.create_patient(db, patient)


@router.get("/{patient_id}", response_model=schemas.PatientWithVaccinations)
async def get_patient(patient_id: int, db: AsyncSession = Depends(get_db)):
    """Получить данные по одному (выбранному) пациенту"""
    db_patient = await crud.get_patient(db, patient_id)
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient
