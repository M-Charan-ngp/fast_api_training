from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.sql import func
from Config.database import Base
from Models.Enrollement import enrollment_association
from sqlalchemy.orm import relationship

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    roll_no = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True)
    date_of_birth = Column(Date)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    courses = relationship(
        "Course", 
        secondary=enrollment_association, 
        back_populates="students",
        lazy="selectin"
    )