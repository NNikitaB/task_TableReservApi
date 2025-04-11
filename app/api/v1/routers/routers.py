from fastapi import APIRouter
from .reservations import reservations_router
from .tables import tables_router
from app.core import logger



routers = APIRouter()


routers.include_router(tables_router)
routers.include_router(reservations_router)


logger.info("routers included")


