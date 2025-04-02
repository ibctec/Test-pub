"""
Test main module API for IO Error
"""
import sys
import os

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from emp.main import app


@pytest.fixture
def client():
    """Test client"""
    client = TestClient(app)
    yield client


@pytest.fixture
def mock_db():
    """Creates a mock database session"""
    mock_session = MagicMock()
    mock_query = mock_session.query.return_value
    mock_filter = mock_query.filter.return_value

    # Mock Employee object
    mock_employee = MagicMock()
    mock_employee.id = 1
    mock_employee.name = "John Doe"

    # Simulate `filter().first()` returning the mock employee
    mock_filter.first.return_value = mock_employee

    return mock_session


def test_io_error_on_create_employee(client: TestClient):
    """Test get_employee by patching get_db()"""
    with patch("emp.main.get_db") as mock_db:
        # mock_db.return_value = mock_db
        mock_db.side_effect = IOError("Database connection failed")

        response = client.post(
            "/employee/",
            json={"name": "John Doe", "email": "test2@example.com"},
        )

        # Assertions
        assert response.status_code == 500
        assert (
            response.json()["detail"]
            == "Error creating Employee due to Database connection error"
        )


def test_io_error_on_get_employee(client: TestClient):
    """Test get_employee by patching get_db() to throw exception"""
    with patch("emp.main.get_db") as mock_db:
        # mock_db.return_value = mock_db
        mock_db.side_effect = IOError("Database connection failed")
        # with pytest.raises(IOError, match="Database connection failed"):

        response = client.get("/employees/")

        # Assertions
        print(f"{response.json()=}")
        assert response.status_code == 500
        assert (
            response.json()["detail"]
            == "Error getting Employees due to Database connection error"
        )
