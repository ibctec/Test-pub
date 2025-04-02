"""
Test main module API
"""
import sys
import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from emp.main import app, get_db
from emp.schemas import Employee  # Import Employee model from actual schemas
from emp.schemas import Base


# Setup test database
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override the get_db dependency
def override_get_db():
    """ Override get_db with in memory """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# Create tables
Base.metadata.create_all(bind=engine)

client = TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def setup_db():
    """Clears the test database before each test."""
    db = TestingSessionLocal()
    db.query(Employee).delete()
    db.commit()
    db.close()


def test_create_employee():
    """Test creating a new employee with a mock db."""

    response = client.post(
        "/employee/",
        json={"name": "John Doe", "email": "test2@example.com"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Employee created successfully"


def test_create_duplicate_employee():
    """Test that duplicate email is not allowed"""
    client.post("/employee/", json={"name": "John Doe", "email": "johndoe@example.com"})
    response = client.post(
        "/employee/", json={"name": "Jane Doe", "email": "johndoe@example.com"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_invalid_email():
    """Test that email is invalid"""
    client.post("/employee/", json={"name": "John Doe", "email": "johndoe@example.com"})
    response = client.post(
        "/employee/", json={"name": "Jane Doe", "email": "johndoeexample.com"}
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == \
        "value is not a valid email address: An email address must have an @-sign."

def test_get_employees():
    """Test getting all employees"""
    client.post("/employee/", json={"name": "John Doe", "email": "johndoe@example.com"})
    client.post("/employee/", json={"name": "Jane Doe", "email": "janedoe@example.com"})

    response = client.get("/employees/")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["email"] == "johndoe@example.com"
    assert response.json()[1]["email"] == "janedoe@example.com"
