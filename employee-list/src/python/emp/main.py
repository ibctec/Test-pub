"""
API application using FastApi for API and 
Sqlite4 for DB to create and list employees

"""

import logging
from typing import Any, Generator

from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session

from emp.models import EmployeeResponse, CreateEmployee

from emp.db import SessionLocal
from emp.schemas import Employee

app = FastAPI()
# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Dependency to get DB session
def get_db() -> Generator[Session, Any, Any]:
    """
    Get the Sqlite DB session

    Returns: DB Session

    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create employee Endpoint
@app.post("/employee/", response_model=dict)
def create_emp(employee: CreateEmployee) -> dict[str, str]:
    """
    Create a new Employee

    Args:
        employee: CreateEmployee
        db: Session

    Raises:
        HTTPException HttpException

    """
    try:
        db = next(get_db())
        if db.query(Employee).filter(Employee.email == employee.email).first():
            logger.error("Email already registered")
            raise HTTPException(status_code=400, detail="Email already registered")

        new_emp = Employee(name=employee.name, email=employee.email)
        db.add(new_emp)
        db.commit()
        db.refresh(new_emp)
        logger.info("Employee created: %s", new_emp.email)
        return {"message": "Employee created successfully", "user_id": new_emp.id}
    except IOError as ioe:
        logger.error("Error creating Employee %s", ioe)
        raise HTTPException(
            status_code=500,
            detail="Error creating Employee due to Database connection error",
        ) from ioe


# Get All Employees Endpoint
@app.get("/employees/", response_model=list[EmployeeResponse])
def get_employees() -> list[Employee]:
    """
    Get a list of all employees

    Args:
        db DB session depends on get_db

    Return:
        list[Employee] List of Employee objects

    """
    try:
        db = next(get_db())
        employees = db.query(Employee).all()
        logger.debug("Employees retrieved: %s", employees)
        return employees
    except IOError as ioe:
        logger.debug("Unexpected error occured %s", ioe)
        raise HTTPException(
            status_code=500,
            detail="Error getting Employees due to Database connection error",
        ) from ioe
