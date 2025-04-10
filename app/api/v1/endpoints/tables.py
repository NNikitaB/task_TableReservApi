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


tables_router = APIRouter(prefix="/api/v1/tables", tags=["Tables"])


@tables_router.post("/tables/", response_model=TableResponse, status_code=status.HTTP_201_CREATED)
async def create_table(table_data: TableCreate, db_session: AsyncSession = Depends(get_async_session)):
    service = TableService(UnitOfWork(db_session))
    try:
        return await service.create_table(table_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@tables_router.get("/tables/{table_id}", response_model=TableResponse)
async def get_table(table_id: int, db_session: AsyncSession = Depends(get_async_session)):
    service = TableService(UnitOfWork(db_session))
    try:
        return await service.get_table(TableGet(id=table_id))
    except TableNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found")



