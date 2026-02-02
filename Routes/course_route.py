from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from Config.database import get_db
from schemas import course as course_schema
from Controllers import course_controller
from Middlewares.jwt_middleware import get_current_user , RoleChecker
from Models.User import UserRole

router = APIRouter(
    prefix="/courses", 
    tags=["Courses"],
    dependencies=[Depends(get_current_user)]
)

admin_only = RoleChecker([UserRole.ADMIN])

@router.get("/", response_model=List[course_schema.Course])
async def get_all(db: AsyncSession = Depends(get_db),page: int = 0, limit: int = 10):
    courses = await course_controller.get_all_courses(db,page,limit)
    if not courses:
        raise HTTPException(
            status_code=404, 
            detail="courses not found"
        )
    return courses

@router.get("/{id}", response_model=course_schema.CourseWithDetails)
async def get_one(id: int, db: AsyncSession = Depends(get_db)):
    course = await course_controller.get_course(db, id)
    if not course:
        raise HTTPException(
            status_code=404, 
            detail="Course not found"
        )
    return course

@router.post("/", response_model=course_schema.Course, status_code=201,dependencies=[Depends(admin_only)])
async def create(course_data: course_schema.CourseCreate, db: AsyncSession = Depends(get_db)):
    course = await course_controller.create_course(db, course_data)
    return course

@router.put("/{id}", response_model=course_schema.Course,dependencies=[Depends(admin_only)])
async def update(id: int, course_data: course_schema.CourseUpdate, db: AsyncSession = Depends(get_db)):
    updated_course = await course_controller.update_course(db, id, course_data)
    if not updated_course:
        raise HTTPException(
            status_code=404, 
            detail="Course not found"
        )
    return updated_course

@router.delete("/{id}", status_code=status.HTTP_200_OK, dependencies=[Depends(admin_only)])
async def delete(id: int, db: AsyncSession = Depends(get_db),):
    success = await course_controller.delete_course(db, id)
    if not success:
        raise HTTPException(
            status_code=404, 
            detail="Course not found"
        )
    return { 
        "status":"success",
        "message": "Course deleted successfully"}

@router.post("/addStudents/{course_id}", dependencies=[Depends(admin_only)])
async def bulk_add_students_to_course(
    course_id: int, 
    enrollment_data: course_schema.BulkEnrollment, 
    db: AsyncSession = Depends(get_db)
):
    added_count,existing_ids = await course_controller.bulk_enroll_students(
        db, course_id, enrollment_data.student_ids
    )
    if added_count is None:
        raise HTTPException(status_code=404, detail="Course not found")
    if added_count ==0:
        raise HTTPException(status_code=409, detail="All the students in the list are already enrolled or id's not available")
    return {
        "status": "success",
        "message": f"Successfully enrolled {added_count} new students, already enrolled or not available students omited",
        "Omitted": existing_ids,
        "total_requested": len(enrollment_data.student_ids)
    }