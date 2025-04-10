from .repository import BaseSqlAsyncRepository
from app.models import Tables
from sqlalchemy.ext.asyncio import AsyncSession


class TableRepository(BaseSqlAsyncRepository[Tables]):

    def __init__(self, session: AsyncSession):
        super().__init__(session,Tables)

    async def get_list_services(self, id):
        """Get list of services for user"""
        table = await self.get_by_identifier(id)
        if table:
            return table.reserved_tables
        return None