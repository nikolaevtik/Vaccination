from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional, List


class PatientBase(BaseModel):
    full_name: str
    birth_date: date
    phone: Optional[str] = None


class PatientCreate(PatientBase):
    pass


class Patient(PatientBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class PatientWithVaccinations(Patient):
    vaccinations: List["Vaccination"] = []


class VaccinationBase(BaseModel):
    patient_id: int
    vaccine_name: str
    dose_number: int
    vaccination_date: date
    next_dose_date: Optional[date] = None


class VaccinationCreate(VaccinationBase):
    pass


class Vaccination(VaccinationBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# Алиасы для роутеров (можно использовать те же имена)
PatientRead = Patient
VaccinationRead = Vaccination
