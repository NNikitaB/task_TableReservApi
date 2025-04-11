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
from datetime import datetime, timedelta
from app.core import logger


class ReservTableService:
    """Service for working with  Reservations of Tables"""
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def _is_check_conflict(self, reserv_data: ReservationCreate) -> bool:
        """Check if reservation time is not conflict

        :param reserv_data: ReservationCreate
        :return: bool False if reservation time is not conflict, True otherwise
        """
        logger.info(f" Checking reservation conflict for table {reserv_data.table_id}")
        start_time = reserv_data.reservation_time
        end_time = start_time + timedelta(minutes=reserv_data.duration_minutes)
        reservs = await self.uow.reservations.get_list_reservs_by_table_id(reserv_data=reserv_data)
        for reserv in reservs:
            if reserv.reservation_time < end_time and \
                reserv.reservation_time + timedelta(minutes=reserv.duration_minutes) > start_time:
                logger.warning(f" Conflict detected for reservation time {reserv_data.reservation_time}")
                return True
        logger.info(" No conflict detected.")
        return False



    async def add_reserv_for_table(self,reserv_data: ReservationCreate) -> ReservationResponse:
        """Add reservation table"""
        logger.info(f" Adding reservation for table {reserv_data.table_id} by {reserv_data.customer_name}")
        async with self.uow:

            table = await self.uow.tables.get_by_identifier(reserv_data.table_id)
            if table is None:
                logger.warning(f" Table with ID {reserv_data.table_id} not found.")
                raise TableNotFound("Table not found")
            
            is_conflict = await self._is_check_conflict(reserv_data=reserv_data)
            if is_conflict:
                logger.error(f" Reservation conflict for table {reserv_data.table_id}.")
                raise TableAlreadyReserv("Conflict with existing reservation")
            
            reserv_table = Reservations(
                table_id=reserv_data.table_id,
                customer_name=reserv_data.customer_name,
                reservation_time=reserv_data.reservation_time,
                duration_minutes=reserv_data.duration_minutes,
                )
            
            res = await self.uow.reservations.add(reserv_table)
            await self.uow.commit()
            logger.info(f" Reservation added for table {reserv_data.table_id}")
            return ReservationResponse.model_validate(res.to_dict())
        
    async def delete_reserv(self,table_data: ReservationGet) -> ReservationResponse:
        """Delete reservation from table"""
        logger.info(f" Deleting reservation with ID {table_data.id}")
        async with self.uow:

            reserv = await self.uow.reservations.get_by_identifier(table_data.id)
            if reserv is None:
                logger.warning(f" Reservation with ID {table_data.id} not found.")
                raise TableNotFound("Reservation not found")

            await self.uow.reservations.delete(table_data.id)
            await self.uow.commit()
            logger.info(f" Reservation with ID {table_data.id} deleted successfully.")
            return ReservationResponse.model_validate(reserv.to_dict())
    
    async def get_all_reserv(self) -> list[ReservationResponse]:
        """Get all reservations"""
        logger.info(" Retrieving all reservations")
        async with self.uow:
            reservs = await self.uow.reservations.list()
        logger.info(f" Retrieved {len(reservs)} reservations.")
        return [ReservationResponse.model_validate(reserv.to_dict()) for reserv in reservs]
    
    async def delete_all_reserv(self) -> None:
        """Delete all reservations"""
        logger.info(" Deleting all reservations")
        async with self.uow:
            reservs = await self.uow.reservations.list()
            for reserv in reservs:
                await self.uow.reservations.delete(reserv.id)
            await self.uow.commit()
        logger.info(" All reservations deleted successfully.")


