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



class TableService:
    """Service for working with data of Tables and Reservations"""
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_table(self, table_data: TableCreate) -> TableResponse:
        """Create new table"""
        async with self.uow:
            new_table = Tables(
                name=table_data.name,
                seats=table_data.seats,
                location=table_data.location,
            )
            await self.uow.tables.add(new_table)
            await self.uow.commit()
        return TableResponse.model_validate(new_table.to_dict())

    async def update_table(self,table_data: TableUpdate) -> TableResponse:
        """Update existing table"""
        async with self.uow:
            table = await self.uow.tables.get_by_identifier(table_data.id)
            if table is None:
                raise TableNotFound("Table not found")
            
            for field, value in table_data.model_dump(exclude_unset=True).items():
                setattr(table, field, value)

            await self.uow.tables.update(table)
            await self.uow.commit()
        return TableResponse.model_validate(table.to_dict())
        
    async def get_table(self, table_data: TableGet) -> TableResponse:
        """Get table by ID"""
        async with self.uow:
            table = await self.uow.tables.get_by_identifier(table_data.id)
            if table is None:
                raise TableNotFound("Table not found")
        return TableResponse.model_validate(table.to_dict())

    async def get_all_tables(self) -> list[TableResponse]:
        """Get all tables"""
        async with self.uow:
            tables = await self.uow.tables.list()
        return [TableResponse.model_validate(table.to_dict()) for table in tables]
    
    async def delete_table(self, table_data: TableGet) -> None:
        """Delete table by ID"""
        async with self.uow:
            await self.uow.tables.delete(table_data.id)
            await self.uow.commit()

    async def delete_all_tables(self) -> None:
        """Delete all tables"""
        async with self.uow:
            tabls = await self.uow.tables.list()
            for t in tabls:
                await self.uow.reservations.delete(t.id)
            await self.uow.commit()


