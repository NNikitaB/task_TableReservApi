import pytest
from sqlalchemy import create_mock_engine,create_engine,delete,update
from sqlalchemy.orm import Session
from app.models import Base, Tables, Reservations
from datetime import  datetime, UTC, timedelta
from sqlalchemy import event


def _fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute('pragma foreign_keys=ON')


def test_create_db():
    """
    Creates a new SQLite database and initializes the database schema.
    """
    url = "sqlite://"
    engine = create_engine(url, echo=True)
    Base.metadata.create_all(engine)


@pytest.fixture(scope="module")
def db_session():
    url="sqlite://"
    engine = create_engine(url,echo=True)
    event.listen(engine, 'connect', _fk_pragma_on_connect)
    Base.metadata.create_all(engine)
    session = Session(bind=engine)
    #session.("PRAGMA foreign_keys = ON") 
    yield session
    session.rollback()
    session.close()


def test_add_table(db_session):
    table = Tables(
        name="table 1",
        seats=5,
        location="terrace",
        )
    s = db_session
    s.add(table)
    s.commit()


def test_get_table(db_session):
    table = Tables(
        name="table 1",
        seats=5,
        location="terrace",
        )
    s = db_session
    s.add(table)
    s.commit()
    table_from_db = s.query(Tables).filter(Tables.id == table.id).first()
    assert table_from_db.id == table.id


def test_delete_table(db_session):
    table = Tables(
        name="table 1",
        seats=5,
        location="terrace",
        )
    s = db_session
    s.add(table)
    s.commit()
    s.execute(delete(Tables).where(Tables.id == table.id))


def test_update_table(db_session):
    table = Tables(
        name="table 1",
        seats=5,
        location="terrace",
        )
    s = db_session
    s.add(table)
    s.commit() 
    s.execute(update(Tables).where(Tables.id == table.id).values(
        name="table 3",
        location="location update",
        seats=7
        )
    )
    table_from_db = s.query(Tables).filter(Tables.id == table.id).first()
    assert table_from_db.id == table.id
    assert table_from_db.seats == 7
    table_from_db.seats = 10
    s.add(table_from_db)
    s.flush()
    s.refresh(table_from_db)
    assert table_from_db.seats == 10


def test_add_table_reservation(db_session):
    table = Tables(
        name="table 1",
        seats=5,
        location="terrace",
        )
    reserv1 = Reservations(customer_name="", reservation_time=datetime.now(UTC),duration_minutes=30, table_id=table.id)
    reserv2 = Reservations(customer_name="", reservation_time=datetime.now(UTC)+timedelta(minutes=30),duration_minutes=30, table_id=table.id)
    table.reserved_tables.append(reserv1)
    table.reserved_tables.append(reserv2)
    s = db_session
    s.add(table)
    s.commit()
    assert len(table.reserved_tables) == 2


def test_get_table_reservation(db_session):
    table = Tables(
        name="table 1",
        seats=5,
        location="terrace",
        )
    reserv1 = Reservations(customer_name="", reservation_time=datetime.now(UTC),duration_minutes=30, table_id=table.id)
    reserv2 = Reservations(customer_name="", reservation_time=datetime.now(UTC)+timedelta(minutes=30),duration_minutes=30, table_id=table.id)
    table.reserved_tables.append(reserv1)
    table.reserved_tables.append(reserv2)
    s = db_session
    s.add(table)
    s.commit()
    reservation_from_db = s.query(Reservations).filter(Reservations.table_id == table.id).all()
    assert len(reservation_from_db) == 2


def test_delete_table_reservation(db_session):
    table = Tables(
        name="table 1",
        seats=5,
        location="terrace",
        )
    reserv1 = Reservations(customer_name="", reservation_time=datetime.now(UTC),duration_minutes=30, table_id=table.id)
    reserv2 = Reservations(customer_name="", reservation_time=datetime.now(UTC)+timedelta(minutes=30),duration_minutes=30, table_id=table.id)
    table.reserved_tables.append(reserv1)
    table.reserved_tables.append(reserv2)
    s = db_session
    s.add(table)
    s.commit()
    s.delete(table)
    s.commit()
    reservation_from_db = s.query(Reservations).filter(Reservations.table_id == table.id).all()
    assert len(reservation_from_db) == 0

