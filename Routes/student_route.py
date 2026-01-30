from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from Config.database import get_db
from schemas import student as student_schema
import Controllers.student_controller as student_controller
from Middlewares.jwt_middleware import get_current_user, RoleChecker,UserRole

router = APIRouter(
    prefix="/students",
    tags=["Students"],
    dependencies=[Depends(get_current_user)]
)
admin_only = RoleChecker([UserRole.ADMIN])

@router.get("/", response_model=List[student_schema.Student])
async def get_students(page: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await student_controller.get_students(db, page=page, limit=limit)

@router.get("/search/{roll_no}", response_model=student_schema.Student)
async def get_by_roll_no(roll_no: str, db: AsyncSession = Depends(get_db)):
    print("hello")
    db_student = await student_controller.get_student_by_roll(db, roll_no)
    if not db_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Student with this roll number not found"
        )
    return db_student

@router.get("/{id}", response_model=student_schema.Student)
async def get_student(id: int, db: AsyncSession = Depends(get_db)):
    db_student = await student_controller.get_student(db, id)
    if not db_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Student not found"
        )
    return db_student

@router.post("/", response_model=student_schema.Student, status_code=status.HTTP_201_CREATED)
async def create_student(student_data: student_schema.StudentCreate, db: AsyncSession = Depends(get_db)):
    student = await student_controller.create_student(db, student_data)
    return student

@router.put("/{id}", response_model=student_schema.Student)
async def update_student(id: int, student_data: student_schema.StudentUpdate, db: AsyncSession = Depends(get_db)):
    db_student = await student_controller.update_student(db, id, student_data)
    if not db_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Student not found"
        )
    return db_student

@router.delete("/{id}")
async def delete_student(id: int, db: AsyncSession = Depends(get_db)):
    success = await student_controller.delete_student(db, id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Student not found"
        )
    return {
        "status":"success",
        "message": "Student deleted successfully"}

@router.post("/enroll",dependencies=[Depends(admin_only)])
async def enroll_student(enrollment: student_schema.EnrollmentCreate, db: AsyncSession = Depends(get_db)):
    result = await student_controller.enroll_student_in_course(db, enrollment)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Either invalid student id or course id"
        )
    
    if result is False:
        return {
            "status": "fail", 
            "message": "Student already enrolled in this course"
        }
    return {
        "status": "success", 
        "message": "Enrollment successful"
    }