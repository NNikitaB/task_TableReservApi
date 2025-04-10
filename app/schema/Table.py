from pydantic import BaseModel, EmailStr
from typing import Optional, List
from app.schema import ReservationGet
from datetime import datetime,UTC

class TableBase(BaseModel):
    name: str
    seats: int
    location: str
    reserved_tables: Optional[List[ReservationGet]] = None
    class ConfigDict:
        from_attributes = True
        schema_extra = {
            "example": {
                "name": "table 2",
                "seats": 3,
                "location": "bar",
                "reserved_tables": None
            }
        }

class TableGet(TableBase):
    pass

class TableCreate(TableBase):
    id : int

class TableUpdate(TableCreate):
    pass

class TableResponse(TableCreate):
    pass
