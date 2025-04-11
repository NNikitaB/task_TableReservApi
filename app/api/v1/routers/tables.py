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
    """
    Create a new table in the database.

    Args:
        table_data (TableCreate): The data used to create a new table
        db_session (AsyncSession, optional): Async database session dependency

    Returns:
        TableResponse: The newly created table

    Raises:
        HTTPException: 404 Not Found if the table is not found
        HTTPException: 500 Internal Server Error if an unexpected error occurs
    """
    logger.info(f" Creating new table with data: {table_data}")
    service = TableService(UnitOfWork(db_session))
    try:
       return await service.create_table(table_data)
    except TableNotFound as e:
       logger.error(" Table not found")
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
       logger.error(f" Error creating table: {str(e)}")
       raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))



@tables_router.get("/", response_model=List[TableResponse])
async def get_all_tables(db_session: AsyncSession = Depends(get_async_session)):
    """
    Retrieve all tables from the database.

    Returns:
        A list of all table responses

    Raises:
        HTTPException: 404 Not Found if an error occurs during table retrieval
    """
    logger.info(" Retrieving all tables")
    service = TableService(UnitOfWork(db_session))
    try:
        return await service.get_all_tables()
    except Exception as e:
        logger.error(f" Error retrieving tables: {str(e)}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e)


@tables_router.delete("/delete_all", status_code=status.HTTP_200_OK)
async def delete_all_table(db_session: AsyncSession = Depends(get_async_session)):
    """
    Delete all tables from the database.

    Args:
        db_session: Async database session dependency

    Returns:
        A dictionary with a success message confirming all tables were deleted

    Raises:
        HTTPException: 404 Not Found if an error occurs during table deletion
    """
    logger.info(" Deleting all tables")
    service = TableService(UnitOfWork(db_session))
    try:
        await service.delete_all_tables()
        logger.info(" All reservations deleted successfully.")
        return {"message": f"All Tables deleted successfully"}
    except Exception as e:
        logger.error(f" Error deleting all tables: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)


@tables_router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_table(id: int, db_session: AsyncSession = Depends(get_async_session)):
    """
    Delete a specific table by its ID.
    
    Args:
        id: The unique identifier of the table to delete
        db_session: Database session dependency
        
    Returns:
        A success message confirming the table deletion
        
    Raises:
        HTTPException: 404 Not Found if the table doesn't exist or other errors occur
    """
    logger.info(f" Deleting table with ID {id}")
    service = TableService(UnitOfWork(db_session))
    table_delete = TableGet(id=id)
    try:
        await service.delete_table(table_delete)
        logger.info(f" Table with ID {id} deleted successfully.")
        return {"message": f"Table id = {id} deleted successfully"}
    except TableNotFound as e:
       logger.error(" Table not found")
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f" Error deleting table with ID {id}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)


