from pydantic import BaseModel, Field
from typing import Optional, List

class StudentRollSchema(BaseModel):
    name: str
    roll_no: str 

    class Config:
        from_attributes = True 

# --- Course Schemas ---
class CourseBase(BaseModel):
    course_code: str = Field(pattern=r"^[A-Z]{2}\d{3}$")
    title: str
    credits: int = 3


class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    course_code: Optional[str] = Field(
        default=None, 
        pattern=r"^[A-Z]{2}\d{3}$"
    )
    title: Optional[str] = None
    credits: Optional[int] = None

class Course(CourseBase):
    id: int

    class Config:
        from_attributes = True

class CourseWithDetails(Course):
    students: List[StudentRollSchema] = []