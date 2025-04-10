from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum
from .Base import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime, UTC


class Reservations(Base):
    """
    SQLAlchemy model representing a restaurant table reservation.

    Attributes:
        id (int): Unique identifier for the reservation.
        customer_name (str): Name of the customer making the reservation.
        table_id (int): Foreign key referencing the reserved table.
        reservation_time (datetime): Timestamp of the reservation, defaults to current UTC time.
        duration_minutes (int): Length of the reservation in minutes, defaults to 60.
        table (relationship): Relationship to the Tables model, allowing bidirectional access.
    """
        
    __tablename__ = "reservations"
    #basic fields
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_name: Mapped[str] = mapped_column(nullable=False)
    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id",ondelete="CASCADE"), nullable=False)
    reservation_time = mapped_column(DateTime(timezone=True), default=datetime.now(UTC))
    duration_minutes: Mapped[int] = mapped_column(Integer, default=60)
    #relationships
    table = relationship("Tables", back_populates="reserved_tables")


    def to_dict(self,exclude_relate=True) -> dict:
        """
        Converts the SQLAlchemy model instance to a dictionary, including its basic attributes.
        Excludes the relationships to avoid recursive structures.
        """
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "table_id": self.table_id,
            "reservation_time": self.reservation_time,
            "duration_minutes": self.duration_minutes,
        }


