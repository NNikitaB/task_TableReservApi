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


reservations_router = APIRouter(prefix="/api/v1/reservations", tags=["Reservations"])


@reservations_router.post("/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
async def create_reservation(reservation_data: ReservationCreate, db_session: AsyncSession = Depends(get_async_session)):
    service = ReservTableService(UnitOfWork(db_session))
    try:
        return await service.add_reserv_for_table(reservation_data)
    except TableNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found")
    except TableAlreadyReserv:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Table already reserved")


@reservations_router.get("/", response_model=List[ReservationResponse])
async def get_all_reservations(db_session: AsyncSession = Depends(get_async_session)):
    service = ReservTableService(UnitOfWork(db_session))
    return await service.get_all_reserv()


@reservations_router.delete("/{id}", response_model=ReservationResponse)
async def delete_reservation(id: int, db_session: AsyncSession = Depends(get_async_session)):
    service = ReservTableService(UnitOfWork(db_session))
    reservation_delete = ReservationGet(id=id)
    try:
        return await service.delete_reserv(reservation_delete)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e)


