import pytest
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
from datetime import datetime, timedelta, UTC


# Test for Reservation schemas
@pytest.fixture
def reservation_data():
    return {
        "customer_name": "Default",
        "duration_minutes": 60,
        "reservation_time": datetime.now(UTC),
        "table_id": 23,
    }


# Test ReservationCreate schema validation
def test_reservation_create(reservation_data):
    reservation_data["id"] = 2
    reserv = ReservationCreate(**reservation_data)
    assert reserv.duration_minutes == 60
    assert reserv.table_id == 23
    assert isinstance(reserv.reservation_time, datetime)

# Test ReservationUpdate schema validation
def test_reservation_update():
    reserv_update = ReservationUpdate(id=1,customer_name="Default",table_id=23)
    assert reserv_update.id == 1
    assert reserv_update.customer_name == "Default"

# Test ReservationGet schema validation
def test_reservation_get(reservation_data):
    reservation_data['id'] = 1
    reserv = ReservationGet(**reservation_data)
    assert reserv.id == 1
   


@pytest.fixture
def table_data():
    return {
        "id": 4,
        "name": "Table john_doe",
        "seats": 2,
        "location": "Test location",
    }


# Test tableCreate schema validation (including hashed_password and created_at)
def test_table_create(table_data):
    table_create = TableCreate(**table_data)
    assert table_create.name == table_data["name"]
    assert table_create.seats == 2
    assert table_create.location == table_create.location


# Test tableUpdate schema validation (optional fields like hashed_password and email_verified)
def test_table_update(table_data):
    table_data['name'] = "test"
    table_update = TableUpdate(**table_data)
    assert table_update.name == "test"


# Test tableGet schema validation (including reservations_access as a list of ReservationGet)
def test_table_get(table_data):
    table_data['reserved_tables'] = [ReservationResponse(id=2,table_id=1, customer_name="John Doe", duration_minutes=60, reservation_time=datetime.now(UTC))]
    table_get = TableCreate(**table_data)
    assert table_get.name == table_data["name"]



# Test tableResponse schema validation (for response containing table details and reservations_access)
def test_table_response(table_data):
    table_data['reserved_tables'] = [
        ReservationResponse(id=1,table_id=table_data["id"], customer_name="John Doe", duration_minutes=60, reservation_time=datetime.now(UTC)),
        ReservationResponse(id=2,table_id=table_data["id"], customer_name="John Doe", duration_minutes=60, reservation_time=datetime.now(UTC)+timedelta(minutes=100)),
        ]
    table_response = TableResponse(**table_data)
    assert table_response.name == table_data["name"]
    assert isinstance(table_response.reserved_tables, list)
    assert len(table_response.reserved_tables) == 2
    assert isinstance(table_response.reserved_tables[0], ReservationResponse)
