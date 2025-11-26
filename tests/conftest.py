import pytest
from fastapi.testclient import TestClient
from handlers import app, db


@pytest.fixture(autouse=True)
def reset_db():
    """Reset the database before each test"""
    db.students = {}
    db.canteens = {}
    db.reservations = {}
    db.canteen_capacities = {}
    db.canteen_reservations = {}
    db.student_reservations = {}
    db.next_student_id = 1
    db.next_canteen_id = 1
    db.next_reservation_id = 1
    db.emails = set()
    db.canteen_locations = set()
    db.canteen_names = set()
    yield


@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)


@pytest.fixture
def admin_student(client):
    """Create an admin student and return the response data"""
    response = client.post(
        "/students",
        json={
            "name": "Admin User",
            "email": "admin@test.com",
            "isAdmin": True
        }
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def regular_student(client):
    """Create a regular student and return the response data"""
    response = client.post(
        "/students",
        json={
            "name": "Regular User",
            "email": "user@test.com",
            "isAdmin": False
        }
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def sample_canteen(client, admin_student):
    """Create a sample canteen and return the response data"""
    response = client.post(
        "/canteens",
        headers={"studentId": str(admin_student["id"])},
        json={
            "name": "Test Canteen",
            "location": "Test Location 1",
            "capacity": 10,
            "workingHours": [
                {"meal": "breakfast", "from": "07:00", "to": "10:00"},
                {"meal": "lunch", "from": "11:00", "to": "15:00"},
                {"meal": "dinner", "from": "17:00", "to": "20:00"}
            ]
        }
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def sample_reservation(client, regular_student, sample_canteen):
    """Create a sample reservation and return the response data"""
    response = client.post(
        "/reservations",
        json={
            "studentId": regular_student["id"],
            "canteenId": sample_canteen["id"],
            "date": "2025-12-15",
            "time": "12:00",
            "duration": 30
        }
    )
    assert response.status_code == 201
    return response.json()
