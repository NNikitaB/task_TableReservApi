from pydantic import BaseModel, EmailStr,Field
from typing import Optional, List
from app.schema import ReservationResponse
from datetime import datetime,UTC

class TableBase(BaseModel):
    name: str
    seats: int = Field(default=4,ge=0)
    location: str
    class ConfigDict:
        from_attributes = True
        schema_extra = {
            "example": {
                "name": "table 2",
                "seats": 3,
                "location": "bar",
            }
        }

class TableGet(BaseModel):
    id: int
    class ConfigDict:
        from_attributes = True

class TableCreate(TableBase):
    pass

class TableUpdate(TableCreate):
    id : int

class TableResponse(TableUpdate):
    reserved_tables: Optional[List[ReservationResponse]] = None
