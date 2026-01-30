from sqlalchemy import Table, Column, Integer, ForeignKey
from Config.database import Base

enrollment_association = Table(
    'enrollments',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id', ondelete="CASCADE"), primary_key=True),
    Column('course_id', Integer, ForeignKey('courses.id', ondelete="CASCADE"), primary_key=True)
)