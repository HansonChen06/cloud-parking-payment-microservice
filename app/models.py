from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4

from sqlalchemy import DateTime, Float, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class PaymentStatus(str, Enum):
    pending = "pending"
    authorized = "authorized"
    failed = "failed"
    refunded = "refunded"


class ParkingSessionStatus(str, Enum):
    active = "active"
    completed = "completed"
    cancelled = "cancelled"


class ParkingSession(Base):
    __tablename__ = "parking_sessions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    license_plate: Mapped[str] = mapped_column(String(16), index=True)
    zone_id: Mapped[str] = mapped_column(String(32), index=True)
    duration_minutes: Mapped[int]
    amount_cents: Mapped[int]
    currency: Mapped[str] = mapped_column(String(3), default="CAD")
    payment_status: Mapped[PaymentStatus] = mapped_column(
        SqlEnum(PaymentStatus), default=PaymentStatus.pending
    )
    session_status: Mapped[ParkingSessionStatus] = mapped_column(
        SqlEnum(ParkingSessionStatus), default=ParkingSessionStatus.active
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
