from pydantic import BaseModel, EmailStr,Field
from typing import Optional, List
from app.schema import ReservationResponse
from datetime import datetime,UTC


class TableBase(BaseModel):
    """
    Base Pydantic model representing a table with essential attributes.

    Defines the core properties of a table including its name, number of seats,
    and location. Provides a default configuration for serialization and an
    example schema for documentation purposes.

    Attributes:
        name (str): The name or identifier of the table.
        seats (int): Number of seats at the table, defaulting to 4 with a minimum of 0.
        location (str): The specific location or area where the table is situated.
    """
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
