from fastapi import APIRouter
from .reservations import reservations_router
from .tables import tables_router


routers = APIRouter()


routers.include_router(tables_router)
routers.include_router(reservations_router)

