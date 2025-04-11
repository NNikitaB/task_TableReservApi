from typing import TYPE_CHECKING
from sqlalchemy.orm import DeclarativeBase,declarative_base


class Base(DeclarativeBase):
    """
    Base declarative model for SQLAlchemy ORM, serving as an abstract base class for database models.

    This class inherits from DeclarativeBase and is marked as abstract, meaning it cannot be instantiated directly.
    Subclasses will inherit its ORM configuration and can define their own table-specific attributes and relationships.
    """
    abstract = True
    