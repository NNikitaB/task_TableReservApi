import pytest
import pytest_asyncio
from sqlalchemy import create_mock_engine,create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine,AsyncSession
from sqlalchemy.orm import Session
from app.models.Base import Base
from app.models import Tables, Reservations
from app.utils.patterns import TableRepository, ReservationRepository, UnitOfWork
from app.schema import (
    TableBase,
    TableCreate,
    TableUpdate,
    TableGet,
    TableResponse,
    ReservationBase,
    ReservationCreate,
    ReservationUpdate,
    ReservationGet,
    ReservationResponse
)
from typing import Sequence
import datetime
import uuid
import asyncio
from sqlalchemy import event
from datetime import datetime, timedelta, UTC
from app.services import ReservTableService,TableService,TableAlreadyReserv,TableNotFound


def _fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute('pragma foreign_keys=ON')


@pytest_asyncio.fixture(scope="function")
async def db_session():
    url="sqlite+aiosqlite://"
    engine = create_async_engine(url=url,echo=True)
    event.listen(engine.sync_engine, 'connect', _fk_pragma_on_connect)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        await session.begin()
        yield session
        await session.rollback()


@pytest.fixture
def table_create_data():
    """Фикстура для данных создания таблицы"""
    return TableCreate(
        name="Table 1",
        seats=4,
        location="Room 1"
    )

@pytest.fixture
def reservation_create_data():
    """Фикстура для данных создания брони"""
    return ReservationCreate(
        table_id=1,
        customer_name="John Doe",
        reservation_time=datetime(2025, 4, 10, 19, 30),
        duration_minutes=60
    )



@pytest.mark.asyncio   
async def test_create_get_table(db_session, table_create_data):
    """Создание таблицы"""
    service = TableService(UnitOfWork(db_session))

    t  = await service.create_table(table_create_data)

    t_added = await service.get_table(TableGet(id=t.id))
    assert t_added is not None


@pytest.mark.asyncio
async def test_update_table(db_session, table_create_data):
    """Тест на обновление таблицы"""
    service = TableService(UnitOfWork(db_session))
    

    table = await service.create_table(table_create_data)
    

    updated_data = TableUpdate(id=table.id, name="Updated Table", seats=6, location="Updated Room")
    updated_table = await service.update_table(updated_data)
    

    assert updated_table.name == "Updated Table"
    assert updated_table.seats == 6
    assert updated_table.location == "Updated Room"



@pytest.mark.asyncio
async def test_get_table(db_session, table_create_data):
    """Тест на получение таблицы"""
    service = TableService(UnitOfWork(db_session))
    
    # Создаем таблицу
    table = await service.create_table(table_create_data)
    
    # Получаем таблицу по ID
    table_get = TableGet(id=table.id)
    retrieved_table = await service.get_table(table_get)
    
    # Проверяем, что таблица была найдена
    assert retrieved_table.id == table.id
    assert retrieved_table.name == table.name
    assert retrieved_table.seats == table.seats
    assert retrieved_table.location == table.location


@pytest.mark.asyncio
async def test_delete_table(db_session, table_create_data):
    """Тест на удаление таблицы"""
    service = TableService(UnitOfWork(db_session))
    
    # Создаем таблицу
    table = await service.create_table(table_create_data)
    
    # Удаляем таблицу
    table_get = TableGet(id=table.id)
    await service.delete_table(table_get)
    
    # Проверяем, что таблица была удалена
    with pytest.raises(TableNotFound):
        await service.get_table(table_get)





#test reservation

@pytest.mark.asyncio
async def test_create_reservation(db_session, reservation_create_data):
    """Тест на создание брони"""
    service = ReservTableService(UnitOfWork(db_session))
    service_table = TableService(UnitOfWork(db_session))
    
    # Создаем таблицу для бронирования
    table_create_data = TableCreate(name="Table 1", seats=4, location="Room 1")
    table = await service_table.create_table(table_create_data)
    
    # Создаем бронь
    reservation_create_data.table_id = table.id  # Связываем бронь с созданной таблицей
    reservation = await service.add_reserv_for_table(reservation_create_data)
    
    # Проверяем, что бронь была создана
    assert reservation.table_id == table.id
    assert reservation.customer_name == reservation_create_data.customer_name
    assert reservation.reservation_time == reservation_create_data.reservation_time
    assert reservation.duration_minutes == reservation_create_data.duration_minutes


@pytest.mark.asyncio
async def test_conflict_reservation(db_session, reservation_create_data):
    """Тест на проверку конфликта брони"""
    service = ReservTableService(UnitOfWork(db_session))
    service_table = TableService(UnitOfWork(db_session))
    # Создаем таблицу для бронирования
    table_create_data = TableCreate(name="Table 1", seats=4, location="Room 1")
    table = await service_table.create_table(table_create_data)
    
    # Создаем первую бронь
    reservation_create_data.table_id = table.id  # Связываем бронь с созданной таблицей
    reservation_1 = await service.add_reserv_for_table(reservation_create_data)
    
    # Пытаемся создать конфликтную бронь
    conflict_reservation_data = ReservationCreate(
        table_id=table.id,
        customer_name="Jane Doe",
        reservation_time=reservation_create_data.reservation_time,  # Время конфликта
        duration_minutes=reservation_create_data.duration_minutes
    )
    
    with pytest.raises(TableAlreadyReserv):
        await service.add_reserv_for_table(conflict_reservation_data)
    

@pytest.mark.asyncio
async def test_get_all_tables(db_session, table_create_data):
    """Тест на получение всех таблиц"""
    service = ReservTableService(UnitOfWork(db_session))
    service_table = TableService(UnitOfWork(db_session))
    # Создаем несколько таблиц
    await service_table.create_table(table_create_data)
    await service_table.create_table(TableCreate(name="Table 2", seats=4, location="Room 2"))
    
    # Получаем все таблицы
    tables = await service_table.get_all_tables()
    
    # Проверяем, что таблицы получены
    assert len(tables) > 1
    assert all(isinstance(table, TableResponse) for table in tables)


@pytest.mark.asyncio
async def test_get_all_reservations(db_session, reservation_create_data):
    """Тест на получение всех бронирований"""
    service = ReservTableService(UnitOfWork(db_session))
    service_table = TableService(UnitOfWork(db_session))
    # Создаем таблицу для бронирования
    table_create_data = TableCreate(name="Table 1", seats=4, location="Room 1")
    table = await service_table.create_table(table_create_data)
    
    # Создаем несколько броней
    reservation_create_data.table_id = table.id
    await service.add_reserv_for_table(reservation_create_data)
    
    # Создаем еще одну бронь
    second_reservation_data = ReservationCreate(
        table_id=table.id,
        customer_name="Alice",
        reservation_time=datetime(2025, 4, 10, 20, 30),
        duration_minutes=60
    )
    await service.add_reserv_for_table(second_reservation_data)
    
    # Получаем все бронирования
    reservations = await service.get_all_reserv()
    
    # Проверяем, что все бронирования были получены
    assert len(reservations) > 1
    assert all(isinstance(reservation, ReservationResponse) for reservation in reservations)
    assert any(reservation.customer_name == "John Doe" for reservation in reservations)
    assert any(reservation.customer_name == "Alice" for reservation in reservations)


@pytest.mark.asyncio
async def test_delete_all_reservations(db_session, reservation_create_data):
    """Тест на удаление всех броней"""
    service = ReservTableService(UnitOfWork(db_session))
    service_table = TableService(UnitOfWork(db_session))
    # Создаем таблицу для бронирования
    table_create_data = TableCreate(name="Table 1", seats=4, location="Room 1")
    table = await service_table.create_table(table_create_data)
    
    # Создаем несколько броней
    reservation_create_data.table_id = table.id
    await service.add_reserv_for_table(reservation_create_data)
    
    second_reservation_data = ReservationCreate(
        table_id=table.id,
        customer_name="Alice",
        reservation_time=datetime(2025, 4, 10, 20, 30),
        duration_minutes=60
    )
    await service.add_reserv_for_table(second_reservation_data)
    
    # Удаляем все бронирования
    await service.delete_all_reserv()
    
    # Проверяем, что все бронирования удалены
    reservations = await service.get_all_reserv()
    assert len(reservations) == 0


