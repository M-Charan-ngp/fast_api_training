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
async def get_all(db: AsyncSession = Depends(get_db)):
    return await course_controller.get_all_courses(db)

@router.get("/{id}", response_model=course_schema.CourseWithDetails)
async def get_one(id: int, db: AsyncSession = Depends(get_db)):
    course = await course_controller.get_course(db, id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Course not found"
        )
    return {
        "status":"success",
        "data": course
    }

@router.post("/", response_model=course_schema.Course, status_code=status.HTTP_201_CREATED)
async def create(course_data: course_schema.CourseCreate, db: AsyncSession = Depends(get_db)):
    course = await course_controller.create_course(db, course_data)
    return {
        "status":"success",
        "data": course
    }

@router.put("/{id}", response_model=course_schema.Course)
async def update(id: int, course_data: course_schema.CourseUpdate, db: AsyncSession = Depends(get_db)):
    updated_course = await course_controller.update_course(db, id, course_data)
    if not updated_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Course not found"
        )
    return {
        "status":"success",
        "data":updated_course
    }

@router.delete("/{id}", status_code=status.HTTP_200_OK, dependencies=[Depends(admin_only)])
async def delete(id: int, db: AsyncSession = Depends(get_db),):
    success = await course_controller.delete_course(db, id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Course not found"
        )
    return { 
        "status":"success",
        "message": "Course deleted successfully"}

@router.get("/course-rolls/{course_id}",dependencies=[Depends(admin_only)]
            )
async def get_entries_by_course(course_id: int, db: AsyncSession = Depends(get_db)):
    course_with_students = await course_controller.get_students_by_course(db, course_id)
    if not course_with_students:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return {
        "status": "success",
        "Data": [{"rollNo": s.roll_no, "Name": s.name} for s in course_with_students.students]
    }