from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class StudentBase(BaseModel):
    name: str
    roll_no: str
    email: EmailStr
    date_of_birth: Optional[date] = None

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    roll_no: Optional[str] = None
    email: Optional[EmailStr] = None
    date_of_birth: Optional[date] = None

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int

class Student(StudentBase):
    id: int

    class Config:
        from_attributes = True 