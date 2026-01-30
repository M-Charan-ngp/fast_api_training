from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from Config.database import Base
from Models.Enrollement import enrollment_association
from sqlalchemy.orm import relationship

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String(50), unique=True)
    title = Column(String(255), nullable=False)
    credits = Column(Integer, default=3)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime, 
        server_default=func.now(), 
        onupdate=func.now(),       
        server_onupdate=func.now()
    )

    students = relationship(
        "Student", 
        secondary=enrollment_association, 
        back_populates="courses",
        lazy="selectin" 
    )