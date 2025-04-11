from pydantic import BaseModel, Field,field_validator
from typing import Optional, List
from datetime import datetime, UTC



class ReservationBase(BaseModel):
    """
    Base Pydantic model for reservation data with default reservation time and duration.

    Attributes:
        reservation_time (datetime): Timestamp of the reservation, defaults to current UTC time.
        duration_minutes (int): Length of the reservation in minutes, must be greater than 0.

    Configures model to support attribute-based instantiation and provides an example schema.
    """
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