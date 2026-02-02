from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,or_
from fastapi import HTTPException
from Models.Student import Student as StudentModel
from Models.Course import Course as CourseModel
from schemas import student as StudentSchema
from sqlalchemy.orm import selectinload

async def create_student(db: AsyncSession, student: StudentSchema.StudentCreate):
    try:
        result = await db.execute(
            select(StudentModel).filter(
                (StudentModel.roll_no == student.roll_no) | 
                (StudentModel.email == student.email)
            )
        )
        if result.scalars().first():
            raise HTTPException(
                status_code=409,
                detail="Student with this Roll Number or Email already exists"
            )

        student_data = student.model_dump()
        db_student = StudentModel(**student_data)
        db.add(db_student)
        await db.commit()
        await db.refresh(db_student)
        return db_student
    except HTTPException as e:
        raise e
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create student record")

# all students
async def get_students(db: AsyncSession, page:int, limit: int):
    try:
        result = await db.execute(
            select(StudentModel).offset(page*limit).limit(limit)
        )
        return result.scalars().all()
    except Exception:
        raise HTTPException(status_code=500, detail="Could not retrieve student list")

# one student
async def get_student(db: AsyncSession, student_id: int):
    try:
        return await db.get(StudentModel, student_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Error fetching student details")

# student by roll number
async def get_student_by_roll(db: AsyncSession, roll_no: StudentSchema.StudentRoll):
    try:
        result = await db.execute(
            select(StudentModel).filter(StudentModel.roll_no == roll_no)
        )
        return result.scalars().first()
    except Exception:
        raise HTTPException(status_code=500, detail="Error searching for roll number")

# update student
async def update_student(db: AsyncSession, student_id: int, student_update: StudentSchema.StudentUpdate):
    try:
        db_student = await db.get(StudentModel, student_id)
        if not db_student:
            return None
        
        update_data = student_update.model_dump(exclude_unset=True)

        if "roll_no" in update_data or "email" in update_data:
            filters = []
            if "roll_no" in update_data:
                filters.append(StudentModel.roll_no == update_data["roll_no"])
            if "email" in update_data:
                filters.append(StudentModel.email == update_data["email"])
            check_stmt = select(StudentModel).filter(
                or_(*filters),
                StudentModel.id != student_id
            )
            existing = await db.execute(check_stmt)
            if existing.scalars().first():
                raise HTTPException(
                    status_code=409,
                    detail="Roll number or Email is already taken by another student"
                )

        for key, value in update_data.items():
            setattr(db_student, key, value)
            
        await db.commit()
        await db.refresh(db_student)
        return db_student
    except HTTPException as e:
        raise e
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update student record")

# Delete Student
async def delete_student(db: AsyncSession, student_id: int):
    try:
        db_student = await db.get(StudentModel, student_id)
        if not db_student:
            return False
        
        await db.delete(db_student)
        await db.commit()
        return True
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while deleting the student")

#only one student in course
async def enroll_student_in_course(db: AsyncSession, enrollment: StudentSchema.EnrollmentCreate):
    try:
        result = await db.execute(
            select(StudentModel)
            .options(selectinload(StudentModel.courses))
            .filter(StudentModel.id == enrollment.student_id)
        )
        student = result.scalars().first()
        course = await db.get(CourseModel, enrollment.course_id)
        
        if not student or not course:
            return None
            
        if course not in student.courses:
            student.courses.append(course)
            await db.commit()
            return True
        
        return False
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Error during course enrollment")