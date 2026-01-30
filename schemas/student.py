from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional

class StudentBase(BaseModel):
    name: str
    roll_no: str = Field(pattern=r"^\d{2}[A-Z]{3}\d{4}$")
    email: EmailStr
    date_of_birth: Optional[date] = None

class StudentRoll(BaseModel):
    roll_no: str = Field(pattern=r"^\d{2}[A-Z]{3}\d{4}$")
class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    roll_no: Optional[str] = Field(default=None,pattern=r"^\d{2}[A-Z]{3}\d{4}$")
    email: Optional[EmailStr] = None
    date_of_birth: Optional[date] = None

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int

class Student(StudentBase):
    id: int

    class Config:
        from_attributes = True 