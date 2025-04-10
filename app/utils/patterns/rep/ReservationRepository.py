from .repository import BaseSqlAsyncRepository
from app.models import Reservations
from app.schema import ReservationCreate, ReservationUpdate, ReservationBase, ReservationResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, and_
from datetime import datetime, timedelta

class ReservationRepository(BaseSqlAsyncRepository[Reservations]):
    def __init__(self, session: AsyncSession):
        super().__init__(session,Reservations)


    async def get_list_reservs_by_table_id(self, reserv_data:ReservationCreate) -> list[ReservationBase]:
        """get list reservation by table id
        
        :param reserv_data: ReservationCreate
        :return: list[ReservationBase]
        """
        stmt = select(Reservations).where(Reservations.table_id == reserv_data.table_id)
        result = await self._session.execute(stmt)
        return [ReservationBase.model_validate(i.to_dict()) for i in result.scalars().all()]

    # async def is_check_conflict(self, reserv_data:ReservationCreate) -> bool:
    #     """Check if reservation time is not conflict
        
    #     :param reserv_data: ReservationCreate
    #     :return: bool False if reservation time is not conflict, True otherwise
    #     """
    #     start_time = reserv_data.reservation_time
    #     end_time = start_time + timedelta(minutes=reserv_data.duration_minutes)
        
    #     stmt = select(Reservations).where(
    #         Reservations.table_id == reserv_data.table_id,
    #         Reservations.reservation_time < end_time,
    #         Reservations.reservation_time +  func.make_interval(0, 0, 0, 0, reserv_data.duration_minutes) > start_time
    #         #Reservations.reservation_time, f'+{reserv_data.duration_minutes} minutes') > start_time
    #     )
    #     result = await self._session.execute(stmt)
    #     return result.scalar_one_or_none() is not None
        

        

