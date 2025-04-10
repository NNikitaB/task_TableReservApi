from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, UTC


class ReservationBase(BaseModel):
    reservation_time: datetime = datetime.now(UTC)
    duration_minutes: int = 60

    class ConfigDict:
        from_attributes = True
        schema_extra = {
            "example": {
                "duration_minutes": 60,
                "reservation_time": "2021-01-01T00:00:00.000000"
            }
        }


class ReservationGet(ReservationBase):
    table_id: int
    customer_name: str


class ReservationCreate(ReservationGet):
    id: int


class ReservationUpdate(ReservationCreate):
    pass


class ReservationResponse(ReservationGet):
    pass