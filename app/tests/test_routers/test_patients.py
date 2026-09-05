# test_routers/test_patients.py

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_create_patient(client: AsyncClient):
    response = await client.post(
        "/patients/",  # <-- добавил слеш
        json={"full_name": "Тестовый Пациент", "birth_date": "1990-01-01"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Тестовый Пациент"
    assert data["birth_date"] == "1990-01-01"
    assert "id" in data


async def test_get_patients(client: AsyncClient):
    await client.post(
        "/patients/", json={"full_name": "Пациент 1", "birth_date": "1990-01-01"}
    )
    await client.post(
        "/patients/", json={"full_name": "Пациент 2", "birth_date": "1995-05-05"}
    )

    response = await client.get("/patients/")  # <-- добавил слеш
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2


async def test_get_patient_not_found(client: AsyncClient):
    response = await client.get("/patients/999")  # <-- добавил слеш
    assert response.status_code == 404
    assert response.json()["detail"] == "Patient not found"
