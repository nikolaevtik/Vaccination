#test_routers/test_vaccinations.py

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

async def test_create_vaccination(client: AsyncClient):
    patient_resp = await client.post(
        "/patients/",  # <-- добавил слеш
        json={"full_name": "Тестовый Пациент", "birth_date": "1990-01-01"}
    )
    patient_id = patient_resp.json()["id"]
    
    response = await client.post(
        "/vaccinations/",  # <-- добавил слеш
        json={
            "patient_id": patient_id,
            "vaccine_name": "COVID-19",
            "dose_number": 1,
            "vaccination_date": "2026-09-02",
            "next_dose_date": "2026-10-02"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["vaccine_name"] == "COVID-19"
    assert data["dose_number"] == 1

async def test_create_vaccination_patient_not_found(client: AsyncClient):
    response = await client.post(
        "/vaccinations/",  # <-- добавил слеш
        json={
            "patient_id": 999,
            "vaccine_name": "COVID-19",
            "dose_number": 1,
            "vaccination_date": "2026-09-02",
            "next_dose_date": "2026-10-02"
        }
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Patient not found"