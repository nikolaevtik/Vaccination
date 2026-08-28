from pydantic import BaseModel
from datetime import date
from typing import Optional

# Patient schemas
class PatientBase(BaseModel):
    full_name: str
    birth_date: date
    phone: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientRead(PatientBase):
    id: int
    created_at: date

    class Config:
        from_attributes = True

# Vaccination schemas
class VaccinationBase(BaseModel):
    vaccine_name: str
    dose_number: int
    vaccination_date: date
    next_dose_date: Optional[date] = None

class VaccinationCreate(VaccinationBase):
    patient_id: int

class VaccinationRead(VaccinationBase):
    id: int
    patient_id: int

    class Config:
        from_attributes = True

# For patient details with history
class PatientWithVaccinations(PatientRead):
    vaccinations: list[VaccinationRead] = []