import pytest
import pytest_asyncio
from sqlalchemy import create_mock_engine,create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine,AsyncSession
from sqlalchemy.exc import PendingRollbackError,IntegrityError
from sqlalchemy.orm import Session
from app.models.Base import Base
from app.models import Tables, Reservations
from app.utils.patterns import TableRepository, ReservationRepository
from typing import Sequence
from sqlalchemy import event
from datetime import datetime, UTC
from app.utils.patterns.uow import UnitOfWork


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
async def test_commit_transaction(db_session):
    """Test access commit """
    create_table = Tables(
        name="table 1",
        seats=5,
        location="terrace",
    )
    created_table = None
    async with UnitOfWork(db_session) as uow:
        # create table
        await uow.tables.add(create_table)

        await uow.commit()

    async with UnitOfWork(db_session) as uow:
        #  get table 
        created_table = await uow.tables.get_by_identifier(create_table.id)

        await uow.commit()
    # Check table add
    assert created_table is not None
    assert created_table.id == create_table.id


@pytest.mark.asyncio
async def test_rollback_transaction(db_session):
    """test rollback"""
    create_table = Tables(
        name="table 1",
        seats=5,
        location="terrace",
    )
    revs = Reservations(
        table_id= 12,
        customer_name="5",
        reservation_time=datetime.now(UTC),
        duration_minutes=10,
    )
    table_added = None
    with pytest.raises(IntegrityError) as exc_info:
        async with UnitOfWork(db_session) as uow:
            # create table
            await uow.tables.add(create_table)
            await uow.commit()

            # error
            await uow.reservations.add(revs)
    print("test rollback OK")
                

    async with UnitOfWork(db_session) as uow:
        #  get table 
        table_added = await uow.reservations.get_by_identifier(revs.id)

    # Check table 
    assert table_added is  None
