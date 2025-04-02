"""
Application models objects
"""

from pydantic import BaseModel, EmailStr


class EmployeeResponse(BaseModel):
    """
    Employee response model

    Args:
        BaseModel
    """

    id: int
    name: str
    email: str


# Pydantic Model for Input Validation
class CreateEmployee(BaseModel):
    """
    Employee create model

    Args:
        BaseModel
    """

    name: str
    email: EmailStr
