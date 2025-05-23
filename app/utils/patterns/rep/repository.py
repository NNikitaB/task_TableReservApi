from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Sequence, Type, Any, Union
from pydantic import BaseModel
from sqlalchemy.sql.expression import Select
from sqlalchemy import select,and_
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
#from sqlalchemy.orm.unitofwork import UOWTransaction
from uuid import UUID
from app.models.Base import Base
from app.core import logger

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T], ABC):
    @abstractmethod
    async def get_by_identifier(self, id: int) -> Optional[T]:
        """
            Retrieve a record by its unique identifier.
        
            Args:
                id ( int): The unique identifier.
        
            Returns:
                Optional[T]: The record matching the identifier, or None if not found.
        """
                
        raise NotImplementedError()

    @abstractmethod
    async def list(self, **filters) -> List[T]:
        """
        Retrieve a list of records based on optional filter criteria.
    
        Args:
            **filters: Keyword arguments representing filter conditions for querying records.
    
        Returns:
            List[T]: A list of records matching the specified filter criteria.
        """
        raise NotImplementedError()

    @abstractmethod
    async def add(self, record: T) -> T:
        """
        Add a new record to the repository.
    
        Args:
            record (T): The record to be added to the repository.
    
        Returns:
            T: The added record, potentially with updated metadata or identifiers.
        """
        raise NotImplementedError()

    @abstractmethod
    async def update(self, record: T) -> T:
        """
        Update an existing record in the repository.
    
        Args:
            record (T): The record to be updated in the repository.
    
        Returns:
            T: The updated record, potentially with modified attributes or metadata.
        """
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, id: int) -> None:
        """
        Delete a record from the repository by its unique identifier.
    
        Args:
            id (int): The unique identifier of the record to be deleted.
        """
        raise NotImplementedError()


class BaseSqlAsyncRepository(BaseRepository[T], ABC):
    _model_cls: Type[T]

    def __init__(self, session: AsyncSession,model_cls:Type[T]) -> None:
        """
        Initialize a new repository instance with a database session and model class.
    
        Args:
            session (AsyncSession): The asynchronous database session for performing database operations.
            model_cls (Type[T]): The model class representing the database table or entity.
        """
        self._session = session
        self._model_cls = model_cls
        logger.debug(f"Initialized {self._model_cls.__name__} repository")

    def _construct_get_stmt(self, id: int) -> Any:
        stmt = select(self._model_cls).where(getattr(self._model_cls, "id") == id)
        logger.debug(f"Constructing get statement for {self._model_cls.__name__} with ID={id}")
        return stmt
    
    async def get_by_identifier(self, id: int) -> Optional[T]:
        stmt = self._construct_get_stmt(id)
        logger.info(f"Fetching {self._model_cls.__name__} by identifier: {id}")
        res = await self._session.execute(stmt)
        return res.scalar_one_or_none()

    def _construct_list_stmt(self, **filters) -> Any:
        stmt = select(self._model_cls)
        where_clauses = []
        for c, v in filters.items():
            if not hasattr(self._model_cls, c):
                logger.error(f"Invalid column name {c} for {self._model_cls.__name__}")
                raise ValueError(f"Invalid column name {c}")
            where_clauses.append(getattr(self._model_cls, c) == v)
        if len(where_clauses) == 1:
            stmt = stmt.where(where_clauses[0])
        elif len(where_clauses) > 1:
            stmt = stmt.where(and_(*where_clauses))
        return stmt

    async def list(self, **filters) -> List[T]:
        logger.info(f"Listing {self._model_cls.__name__} with filters: {filters}")
        stmt = self._construct_list_stmt(**filters)
        res = await self._session.execute(stmt)
        return list(res.scalars().all())

    async def add(self, record: T) -> T:
        logger.info(f"Adding new {self._model_cls.__name__}: {record}")
        self._session.add(record)
        await self._session.flush()
        await self._session.refresh(record)
        logger.info(f"Added {self._model_cls.__name__}: {record}")
        return record

    async def update(self, record: T) -> T:
        logger.info(f"Updating {self._model_cls.__name__}: {record}")
        self._session.add(record)
        await self._session.flush()
        await self._session.refresh(record)
        logger.info(f"Updated {self._model_cls.__name__}: {record}")
        return record

    async def delete(self, id: int) -> None:
        logger.info(f"Deleting {self._model_cls.__name__} with ID={id}")
        record = await self.get_by_identifier(id)
        if record is not None:
            await self._session.delete(record)
            await self._session.flush()

