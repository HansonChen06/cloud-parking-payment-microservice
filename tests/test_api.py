from __future__ import annotations

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db() -> Generator[Session, None, None]:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


def test_health_check(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_and_get_parking_session(client: TestClient) -> None:
    create_response = client.post(
        "/sessions",
        json={
            "license_plate": "ABC123",
            "zone_id": "VAN-YALETOWN-01",
            "duration_minutes": 90,
            "amount_cents": 550,
            "currency": "CAD",
        },
    )

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["payment_status"] == "pending"
    assert created["session_status"] == "active"

    get_response = client.get(f"/sessions/{created['id']}")

    assert get_response.status_code == 200
    assert get_response.json()["license_plate"] == "ABC123"


def test_update_payment_status(client: TestClient) -> None:
    created = client.post(
        "/sessions",
        json={
            "license_plate": "PAY777",
            "zone_id": "VAN-DOWNTOWN-03",
            "duration_minutes": 60,
            "amount_cents": 400,
        },
    ).json()

    response = client.patch(
        f"/sessions/{created['id']}/payment",
        json={"payment_status": "authorized"},
    )

    assert response.status_code == 200
    assert response.json()["payment_status"] == "authorized"


def test_list_sessions_by_license_plate(client: TestClient) -> None:
    client.post(
        "/sessions",
        json={
            "license_plate": "FILTER1",
            "zone_id": "VAN-KITS-01",
            "duration_minutes": 120,
            "amount_cents": 700,
        },
    )
    client.post(
        "/sessions",
        json={
            "license_plate": "OTHER1",
            "zone_id": "VAN-KITS-01",
            "duration_minutes": 30,
            "amount_cents": 250,
        },
    )

    response = client.get("/sessions", params={"license_plate": "FILTER1"})

    assert response.status_code == 200
    sessions = response.json()
    assert len(sessions) == 1
    assert sessions[0]["license_plate"] == "FILTER1"


def test_missing_session_returns_404(client: TestClient) -> None:
    response = client.get("/sessions/not-a-real-session")

    assert response.status_code == 404
    assert response.json()["detail"] == "Session not found"


def test_invalid_duration_returns_422(client: TestClient) -> None:
    response = client.post(
        "/sessions",
        json={
            "license_plate": "BAD123",
            "zone_id": "VAN-YALETOWN-01",
            "duration_minutes": 0,
            "amount_cents": 550,
        },
    )

    assert response.status_code == 422
