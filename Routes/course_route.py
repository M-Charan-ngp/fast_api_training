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
async def bulk_enroll(course_id: int, data: course_schema.BulkEnrollment, db: AsyncSession = Depends(get_db)):
    # 1. Call Controller
    result = await course_controller.bulk_enroll_students(db, course_id, data.student_ids)

    if result.get("error") == "course_not_found":
        raise HTTPException(status_code=404, detail="Course not found")
    if len(result['new_ids'])==0:
        raise HTTPException(
            status_code=409, 
            detail="All student id's or either not available or already enrolled")

    return {
        "status": "Success",
        "message": f"Successfully added {len(result['new_ids'])} students",
        "details": {
            "enrolled": result["new_ids"],
            "skipped": result["already_enrolled"],
            "not_found": result["missing"]
        }
    }