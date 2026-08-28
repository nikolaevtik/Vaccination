#models.py

from sqlalchemy import Column, Integer, String, Date, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    phone = Column(String, nullable=True)
    created_at = Column(Date, server_default=func.current_date())
    vaccinations = relationship("Vaccination", back_populates="patient")

class Vaccination(Base):
    __tablename__ = "vaccinations"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    vaccine_name = Column(String, nullable=False)
    dose_number = Column(Integer, nullable=False)
    vaccination_date = Column(Date, nullable=False)
    next_dose_date = Column(Date, nullable=True)
    patient = relationship("Patient", back_populates="vaccinations")