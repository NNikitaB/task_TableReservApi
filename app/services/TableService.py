from app.schema import (
    TableCreate,
    TableGet,
    TableUpdate,
    TableBase,
    TableResponse,
    ReservationCreate,
    ReservationGet,
    ReservationUpdate,
    ReservationBase,
    ReservationResponse,
)
from app.models import Tables, Reservations
from app.utils.patterns import IUnitOfWork, UnitOfWork
from app.services.expt import TableNotFound, TableAlreadyReserv
from app.core import logger


class TableService:
    """Service for working with data of Tables and Reservations"""
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_table(self, table_data: TableCreate) -> TableResponse:
        """Create new table"""
        logger.info(f" Creating new table: {table_data.name}")
        async with self.uow:
            new_table = Tables(
                name=table_data.name,
                seats=table_data.seats,
                location=table_data.location,
            )
            await self.uow.tables.add(new_table)
            await self.uow.commit()
            logger.info(f" Table created successfully: {new_table.id} - {new_table.name}")
        return TableResponse.model_validate(new_table.to_dict())

    async def update_table(self,table_data: TableUpdate) -> TableResponse:
        """Update existing table"""
        logger.info(f" Updating table with ID {table_data.id}")
        async with self.uow:
            table = await self.uow.tables.get_by_identifier(table_data.id)
            if table is None:
                logger.warning(f" Table with ID {table_data.id} not found.")
                raise TableNotFound("Table not found")
            
            for field, value in table_data.model_dump(exclude_unset=True).items():
                setattr(table, field, value)

            await self.uow.tables.update(table)
            await self.uow.commit()
            logger.info(f" Table updated successfully: {table.id} - {table.name}")
        return TableResponse.model_validate(table.to_dict())
        
    async def get_table(self, table_data: TableGet) -> TableResponse:
        """Get table by ID"""
        logger.info(f" Retrieving table with ID {table_data.id}")
        async with self.uow:
            table = await self.uow.tables.get_by_identifier(table_data.id)
            if table is None:
                logger.warning(f" Table with ID {table_data.id} not found.")
                raise TableNotFound("Table not found")
            logger.info(f" Table retrieved: {table.id} - {table.name}")
        return TableResponse.model_validate(table.to_dict())

    async def get_all_tables(self) -> list[TableResponse]:
        """Get all tables"""
        logger.info(" Retrieving all tables")
        async with self.uow:
            tables = await self.uow.tables.list()
        logger.info(f" Retrieved {len(tables)} tables.")
        return [TableResponse.model_validate(table.to_dict()) for table in tables]
    
    async def delete_table(self, table_data: TableGet) -> None:
        """Delete table by ID"""
        logger.info(f" Deleting table with ID {table_data.id}")
        async with self.uow:
            await self.uow.tables.delete(table_data.id)
            await self.uow.commit()
            logger.info(f" Table with ID {table_data.id} deleted successfully.")

    async def delete_all_tables(self) -> None:
        logger.info(" Deleting all tables")
        """Delete all tables"""
        async with self.uow:
            tabls = await self.uow.tables.list()
            for t in tabls:
                await self.uow.reservations.delete(t.id)
            await self.uow.commit()
            logger.info(f" Deleted all tables and related reservations.")


