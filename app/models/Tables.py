from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime,Enum
from .Base import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column


class Tables(Base):
    """
    SQLAlchemy ORM model representing tables in the system.
    
    Defines the database schema for table information with fields for basic table details
    and relationships to reservations.
    
    Attributes:
        id (int): Unique primary key identifier for the table
        name (str): Name of the table (required)
        seats (int): Number of seats at the table (required)
        location (str): Location of the table (required)
        reserved_tables: Relationship to reservations associated with the table
    """

    __tablename__ = 'tables'
    #basic fields 
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)  
    name: Mapped[str] = mapped_column(nullable=False,default="Unknown")
    seats: Mapped[int] = mapped_column(nullable=False,default=1)
    location: Mapped[str] = mapped_column(nullable=False,default="Default")
    #relationships
    reserved_tables = relationship("Reservations",back_populates="table",cascade="all, delete",passive_deletes=True, lazy="selectin")


