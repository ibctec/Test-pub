"""
API application using FastApi for API and 
Sqlite4 for DB to create and list employees

"""

import logging
from typing import Any, Generator

from fastapi import FastAPI, HTTPException, Depends
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
def create_emp(
    employee: CreateEmployee, db: Session = Depends(get_db)
) -> dict[str, str]:
    """
    Create a new Employee

    Args:
        employee: CreateEmployee
        db: Session

    Raises:
        HTTPException HttpException

    """
    if db.query(Employee).filter(Employee.email == employee.email).first():
        logger.error("Email already registered")
        raise HTTPException(status_code=400, detail="Email already registered")

    try:
        new_emp = Employee(name=employee.name, email=employee.email)
        db.add(new_emp)
        db.commit()
        db.refresh(new_emp)
        logger.info("Employee created: %s", new_emp.email)
        return {"message": "Employee created successfully", "user_id": new_emp.id}
    except IOError as e:
        logger.error("Error creating Employee %s", e)
        raise IOError(e) from e


# Get All Employees Endpoint
@app.get("/employees/", response_model=list[EmployeeResponse])
def get_employees(db: Session = Depends(get_db)) -> list[Employee]:
    """
    Get a list of all employees

    Args:
        db DB session depends on get_db

    Return:
        list[Employee] List of Employee objects

    """
    try:
        employees = db.query(Employee).all()
        logger.debug("Employees retrieved: %s", employees)
        return employees
    except IOError as e:
        logger.debug("Unexpected error occured %s", e)
        raise IOError(e) from e
