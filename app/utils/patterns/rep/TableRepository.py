from .repository import BaseSqlAsyncRepository
from app.models import Tables
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import logger


class TableRepository(BaseSqlAsyncRepository[Tables]):

    def __init__(self, session: AsyncSession):
        super().__init__(session,Tables)
        logger.debug("Initialized Table repository")

#    async def get_list_reservs(self, id):
#        """Get list of reservs for table"""
#        table = await self.get_by_identifier(id)
#        if table:
#            return table.reserved_tables
#        return None