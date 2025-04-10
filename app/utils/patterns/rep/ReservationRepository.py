from .repository import BaseSqlAsyncRepository
from app.models import Reservations
from sqlalchemy.ext.asyncio import AsyncSession

class ReservationRepository(BaseSqlAsyncRepository[Reservations]):
    def __init__(self, session: AsyncSession):
        super().__init__(session,Reservations)
    

    

