import pytest
import pytest_asyncio
from sqlalchemy import create_mock_engine,create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine,AsyncSession
from sqlalchemy.orm import Session
from app.models.Base import Base
from app.models import Tables, Reservations
from app.utils.patterns import TableRepository, ReservationRepository
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


@pytest.mark.asyncio
async def test_add_table_repos(db_session):
    rep = TableRepository(db_session)
    table = Tables(
        name="table 1",
        seats=5,
        location="terrace",
    )
    await rep.add(table)  
    tables = await rep.list()
    print(f'tables count: {len(tables)}')
    assert len(tables) == 1


@pytest.mark.asyncio
async def test_get_table_repos(db_session):
    rep = TableRepository(db_session)
    table = Tables(
        name="table 1",
        seats=5,
        location="terrace",
    )
    t = await rep.add(table) 
    t_by_id = await rep.get_by_identifier(t.id)
    assert t_by_id is not None
    if t_by_id is not None:
        assert t_by_id.seats == 5
    print(t_by_id)

@pytest.mark.asyncio
async def test_update_table_repos(db_session):
    rep = TableRepository(db_session)
    table = Tables(
        name="table 1",
        seats=5,
        location="terrace",
        id=22
    )
    t = await rep.add(table) 
    t.seats = 1000
    table = await rep.update(t)
    assert table is not None
    assert table.seats == 1000


@pytest.mark.asyncio   
async def test_delete_table_repos(db_session):
    rep = TableRepository(db_session)
    table = Tables(
        name="table 1",
        seats=5,
        location="terrace",
        id=22
    )
    t = await rep.add(table) 
    assert t.id is not None
    await rep.delete(22)
    #with pytest.raises(Exception):
    deleted = await rep.get_by_identifier(22)
    assert deleted is None


@pytest.mark.asyncio    
async def test_get_all_table_repos(db_session):
    rep = TableRepository(db_session)
    n = 10 
    #create n tables
    for i in range(n):
        await rep.add(Tables(name=f"Table {i}",seats=4,location="Test"))
    tables = await rep.list()
    assert tables is not None
    assert len(tables) == n


