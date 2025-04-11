from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.patterns import UnitOfWork
from app.schema import TableCreate, TableUpdate, TableGet, TableResponse, ReservationCreate, ReservationResponse, ReservationGet
from app.models import Tables, Reservations
from app.services import TableNotFound, TableAlreadyReserv
from app.services import ReservTableService, TableService
from typing import List
from fastapi import APIRouter
from app.database.db import get_async_session
from app.core import logger



tables_router = APIRouter(prefix="/api/v1/tables", tags=["Tables"])


@tables_router.post("/", response_model=TableResponse, status_code=status.HTTP_201_CREATED)
async def create_table(table_data: TableCreate, db_session: AsyncSession = Depends(get_async_session)):
    logger.info(f"🔧 Creating new table with data: {table_data}")
    service = TableService(UnitOfWork(db_session))
    try:
       return await service.create_table(table_data)
    except Exception as e:
       logger.error(f"❌ Error creating table: {str(e)}")
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@tables_router.get("/", response_model=List[TableResponse])
async def get_all_tables(db_session: AsyncSession = Depends(get_async_session)):
    logger.info("🔄 Retrieving all tables")
    service = TableService(UnitOfWork(db_session))
    try:
        return await service.get_all_tables()
    except Exception as e:
        logger.error(f"❌ Error retrieving tables: {str(e)}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e)


@tables_router.delete("/delete_all", status_code=status.HTTP_200_OK)
async def delete_all_table(db_session: AsyncSession = Depends(get_async_session)):
    logger.info("🗑️ Deleting all tables")
    service = TableService(UnitOfWork(db_session))
    try:
        await service.delete_all_tables()
        return {"message": f"All Tables deleted successfully"}
    except Exception as e:
        logger.error(f"❌ Error deleting all tables: {str(e)}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e)


@tables_router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_table(id: int, db_session: AsyncSession = Depends(get_async_session)):
    logger.info(f"🗑️ Deleting table with ID {id}")
    service = TableService(UnitOfWork(db_session))
    table_delete = TableGet(id=id)
    try:
        await service.delete_table(table_delete)
        logger.info(f"✅ Table with ID {id} deleted successfully.")
        return {"message": f"Table id = {id} deleted successfully"}
    except Exception as e:
        logger.error(f"❌ Error deleting table with ID {id}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e)


