from sqlalchemy.ext.asyncio import AsyncSession
from typing import Callable
from abc import ABC, abstractmethod
from typing import Protocol
from app.utils.patterns.rep import TableRepository, ReservationRepository
from app.core import logger

class IUnitOfWork(ABC):
    """Интерфейс Unit of Work для управления транзакциями"""

    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def __aenter__(self):
        """Начало контекста Unit of Work"""
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Завершение контекста Unit of Work"""
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        """Фиксация транзакции"""
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        """Откат транзакции"""
        raise NotImplementedError
    

class UnitOfWork(IUnitOfWork):
    """Unit of Work для управления транзакциями """

    def __init__(self, session: AsyncSession):
        logger.debug("UnitOfWork initialized")
        super().__init__(session)
        self.tables = TableRepository(session)  # Подключаем репозиторий столов
        self.reservations = ReservationRepository(session)  # Подключаем репозиторий брони

    async def __aenter__(self):
        """Начинаем транзакцию"""
        logger.info("Starting transaction")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Коммитим или откатываем транзакцию в зависимости от наличия ошибок"""
        if exc_type:
            logger.warning(f"Exception occurred: {exc_type} - {exc_val}, performing rollback")
            await self.rollback()
        else:
            logger.info("No exception, committing transaction")
            await self.commit()

    async def commit(self):
        """Фиксация транзакции"""
        logger.info("Committing transaction")
        await self.session.commit()

    async def rollback(self):
        """Откат транзакции"""
        logger.info("Rolling back transaction")
        await self.session.rollback()
        