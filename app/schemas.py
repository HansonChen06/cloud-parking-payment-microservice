from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models import ParkingSessionStatus, PaymentStatus


class ParkingSessionCreate(BaseModel):
    license_plate: str = Field(min_length=2, max_length=16, examples=["ABC123"])
    zone_id: str = Field(min_length=2, max_length=32, examples=["VAN-YALETOWN-01"])
    duration_minutes: int = Field(gt=0, le=1440, examples=[120])
    amount_cents: int = Field(gt=0, examples=[650])
    currency: str = Field(default="CAD", min_length=3, max_length=3)
    latitude: Optional[float] = Field(default=None, ge=-90, le=90)
    longitude: Optional[float] = Field(default=None, ge=-180, le=180)


class ParkingSessionRead(BaseModel):
    id: str
    license_plate: str
    zone_id: str
    duration_minutes: int
    amount_cents: int
    currency: str
    payment_status: PaymentStatus
    session_status: ParkingSessionStatus
    created_at: datetime
    updated_at: datetime
    latitude: Optional[float]
    longitude: Optional[float]

    model_config = ConfigDict(from_attributes=True)


class PaymentStatusUpdate(BaseModel):
    payment_status: PaymentStatus


class HealthRead(BaseModel):
    status: str
    service: str
    environment: str
