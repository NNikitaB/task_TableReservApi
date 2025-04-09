from pydantic import BaseModel, EmailStr
from typing import Optional, List
from app.schema import ReservationGet
from datetime import datetime,UTC

class TableBase(BaseModel):
    name: str
    seats: int
    location: str
    reserved_tables: Optional[List[ReservationGet]] = None

class TableGet(TableBase):
    pass

class TableCreate(TableBase):
    id : int

class TableUpdate(TableCreate):
    pass

class TableResponse(TableCreate):
    pass
