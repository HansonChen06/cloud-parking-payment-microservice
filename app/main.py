from __future__ import annotations

import logging
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import Base, engine, get_db
from app.logging_config import configure_logging
from app.models import ParkingSession
from app.schemas import (
    HealthRead,
    ParkingSessionCreate,
    ParkingSessionRead,
    PaymentStatusUpdate,
)

settings = get_settings()
configure_logging(settings.log_level)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cloud Parking Payment Microservice",
    version="1.0.0",
    description=(
        "REST API for parking session creation, payment status tracking, "
        "and transaction lookup."
    ),
)


@app.get("/health", response_model=HealthRead, tags=["operations"])
def health() -> HealthRead:
    return HealthRead(
        status="ok",
        service=settings.app_name,
        environment=settings.environment,
    )


@app.post(
    "/sessions",
    response_model=ParkingSessionRead,
    status_code=status.HTTP_201_CREATED,
    tags=["parking sessions"],
)
def create_session(
    payload: ParkingSessionCreate,
    db: Session = Depends(get_db),
) -> ParkingSession:
    session = ParkingSession(**payload.model_dump())
    db.add(session)
    db.commit()
    db.refresh(session)
    logger.info(
        "parking_session_created",
        extra={"session_id": session.id, "zone_id": session.zone_id},
    )
    return session


@app.get("/sessions/{session_id}", response_model=ParkingSessionRead, tags=["parking sessions"])
def get_session(session_id: str, db: Session = Depends(get_db)) -> ParkingSession:
    session = db.get(ParkingSession, session_id)
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    return session


@app.get("/sessions", response_model=list[ParkingSessionRead], tags=["parking sessions"])
def list_sessions(
    license_plate: Optional[str] = Query(default=None, min_length=2, max_length=16),
    zone_id: Optional[str] = Query(default=None, min_length=2, max_length=32),
    limit: int = Query(default=25, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[ParkingSession]:
    statement = select(ParkingSession).order_by(ParkingSession.created_at.desc()).limit(limit)
    if license_plate:
        statement = statement.where(ParkingSession.license_plate == license_plate)
    if zone_id:
        statement = statement.where(ParkingSession.zone_id == zone_id)
    return list(db.scalars(statement))


@app.patch(
    "/sessions/{session_id}/payment",
    response_model=ParkingSessionRead,
    tags=["payments"],
)
def update_payment_status(
    session_id: str,
    payload: PaymentStatusUpdate,
    db: Session = Depends(get_db),
) -> ParkingSession:
    session = db.get(ParkingSession, session_id)
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    session.payment_status = payload.payment_status
    db.commit()
    db.refresh(session)
    logger.info(
        "payment_status_updated",
        extra={"session_id": session.id, "payment_status": session.payment_status.value},
    )
    return session
