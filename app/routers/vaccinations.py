# routers/vaccination.py

from urllib import response

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/vaccinations", tags=["vaccinations"])


@router.post("/", response_model=schemas.VaccinationRead)
async def create_vaccination(
    vacc: schemas.VaccinationCreate, db: AsyncSession = Depends(get_db)
):
    # Проверка существования пациента
    patient = await crud.get_patient(db, vacc.patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return await crud.create_vaccination(db, vacc)


@router.get("/patient/{patient_id}", response_model=list[schemas.VaccinationRead])
async def get_patient_vaccinations(patient_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_vaccinations_by_patient(db, patient_id)
