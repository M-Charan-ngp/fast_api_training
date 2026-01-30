from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from Models.Course import Course as CourseModel
from schemas import course as course_schema

async def get_all_courses(db: AsyncSession, page: int = 0, limit: int = 10):
    try:
        result = await db.execute(
            select(CourseModel).offset(page * limit).limit(limit)
        )
        return result.scalars().all()
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error while fetching courses")

async def get_course(db: AsyncSession, course_id: int):
    try:
        result = await db.execute(
            select(CourseModel)
            .options(selectinload(CourseModel.students))
            .filter(CourseModel.id == course_id)
        )
        return result.scalars().first()
    except Exception:
        raise HTTPException(status_code=500, detail="Error retrieving course details")

async def create_course(db: AsyncSession, course: course_schema.CourseCreate):
    try:
        result = await db.execute(
            select(CourseModel).filter(CourseModel.course_code == course.course_code)
        )
        if result.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Course code already exists"
            )
        db_course = CourseModel(**course.model_dump())
        db.add(db_course)
        await db.commit()
        await db.refresh(db_course)
        return db_course
    except HTTPException as e:
        raise e
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create course")

async def update_course(db: AsyncSession, id: int, course_data: course_schema.CourseUpdate):
    try:
        db_course = await db.get(CourseModel, id)
        if not db_course:
            return None
        update_dict = course_data.model_dump(exclude_unset=True)
        if "course_code" in update_dict:
            new_code = update_dict["course_code"]
            result = await db.execute(
                select(CourseModel).filter(
                    CourseModel.course_code == new_code, 
                    CourseModel.id != id
                )
            )
            if result.scalars().first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="Course code already exists"
                ) 
        stmt = (
            update(CourseModel)
            .where(CourseModel.id == id)
            .values(**update_dict)
            .execution_options(synchronize_session="fetch")
        )  
        await db.execute(stmt)
        await db.commit()
        await db.refresh(db_course)
        return db_course
    except HTTPException as e:
        raise e
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error during update")

async def delete_course(db: AsyncSession, id: int):
    try:
        db_course = await db.get(CourseModel, id)
        if not db_course:
            return False
            
        await db.delete(db_course)
        await db.commit()
        return True
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete course")

async def get_students_by_course(db: AsyncSession, course_id: int):
    try:
        result = await db.execute(
            select(CourseModel)
            .options(selectinload(CourseModel.students))
            .filter(CourseModel.id == course_id)
        )
        return result.scalars().first()
    except Exception:
        raise HTTPException(status_code=500, detail="Database error")