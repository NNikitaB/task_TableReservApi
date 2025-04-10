from pydantic import BaseModel, Field,field_validator
from typing import Optional, List
from datetime import datetime, UTC


class ReservationBase(BaseModel):
    reservation_time: datetime = datetime.now(UTC)
    duration_minutes: int = Field(default=60, gt=0)

    class ConfigDict:
        from_attributes = True
        schema_extra = {
            "example": {
                "duration_minutes": 60,
                "reservation_time": "2021-01-01T00:00:00.000000"
            }
        }


class ReservationGet(BaseModel):
    id: int = Field(..., ge=0)
    
    class ConfigDict:
        from_attributes = True


class ReservationCreate(ReservationBase):
    table_id: int= Field(..., ge=0)
    customer_name: str


class ReservationUpdate(ReservationCreate):
    id: int


class ReservationResponse(ReservationUpdate):
    pass