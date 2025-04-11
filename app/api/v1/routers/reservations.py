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



reservations_router = APIRouter(prefix="/api/v1/reservations", tags=["Reservations"])



@reservations_router.post("/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
async def create_reservation(reservation_data: ReservationCreate, db_session: AsyncSession = Depends(get_async_session)):
    """
    Create a new table reservation.

    Creates a reservation for a specific table with the provided reservation details.
    Handles various potential errors such as table not found or table already reserved.
    checks if the table is already reserved by Date and if not, creates a new reservation.

    Args:
        reservation_data (ReservationCreate): Details of the reservation to be created.
        db_session (AsyncSession, optional): Database session for transaction. Defaults to dependency injection.

    Returns:
        ReservationResponse: The successfully created reservation.

    Raises:
        HTTPException: 404 if table is not found, 400 if table is already reserved,
        HTTPException: 409 if reservation time conflicts with existing reservation.
        HTTPException: 500 for other unexpected errors.
    """

    logger.info(f" Creating reservation with data: {reservation_data}")
    service = ReservTableService(UnitOfWork(db_session))
    try:
        result =  await service.add_reserv_for_table(reservation_data)
        logger.info(f" Reservation created successfully: {result}")
        return result
    except TableNotFound:
        logger.error(f" Table not found for reservation: {reservation_data.table_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found")
    except TableAlreadyReserv:
        logger.error(f" Conflict: Table already reserved at {reservation_data.reservation_time}")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Conflict: Table to Date already reserved")
    except Exception as e:
        logger.error(f" Error creating reservation: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)


@reservations_router.get("/", response_model=List[ReservationResponse])
async def get_all_reservations(db_session: AsyncSession = Depends(get_async_session)):
    """
    Retrieve all table reservations.

    Fetches a list of all existing reservations from the database.

    Args:
        db_session (AsyncSession, optional): Database session for transaction. Defaults to dependency injection.

    Returns:
        List[ReservationResponse]: A list of all current reservations.

    Raises:
        HTTPException: 500 for other unexpected errors.
    """
    logger.info(" Retrieving all reservations")
    service = ReservTableService(UnitOfWork(db_session))
    try:
        reservs = await service.get_all_reserv()
        logger.info(f" Retrieved {len(reservs)} reservations.")
        return reservs
    except Exception as e:
        logger.error(f" Error retrieving reservations: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



@reservations_router.delete("/delete_all", status_code=status.HTTP_200_OK)
async def delete_all_table(db_session: AsyncSession = Depends(get_async_session)):
    """
    Delete all table reservations.

    Removes all existing reservations from the database.

    Args:
        db_session (AsyncSession, optional): Database session for transaction. Defaults to dependency injection.

    Returns:
        dict: A message confirming successful deletion of all reservations.

    Raises:
        HTTPException: 500 if  an error occurs during deletion.
    """
    logger.info(" Deleting all reservations")
    service = ReservTableService(UnitOfWork(db_session))
    try:
        await service.delete_all_reserv()
        logger.info(" All reservations deleted successfully.")
        return {"message": f"All Reservation deleted successfully"}
    except Exception as e:
        logger.error(f" Error deleting all reservations: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)


@reservations_router.delete("/{id}", response_model=ReservationResponse)
async def delete_reservation(id: int, db_session: AsyncSession = Depends(get_async_session)):
    """
    Delete a specific table reservation by its ID.

    Args:
        id (int): The unique identifier of the reservation to be deleted.
        db_session (AsyncSession, optional): Database session for transaction. Defaults to dependency injection.

    Returns:
        ReservationResponse: The details of the deleted reservation.

    Raises:
        HTTPException: 500 for unexpected errors during reservation deletion.
    """
    logger.info(f" Deleting reservation with ID {id}")
    service = ReservTableService(UnitOfWork(db_session))
    reservation_delete = ReservationGet(id=id)
    try:
        result = await service.delete_reserv(reservation_delete)
        logger.info(f" Reservation with ID {id} deleted successfully.")
        return result
    except Exception as e:
        logger.error(f" Error deleting reservation with ID {id}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)


