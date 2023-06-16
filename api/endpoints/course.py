from fastapi import APIRouter, Form, HTTPException, Query, Request, status
from fastapi.responses import JSONResponse
from typing import Optional, List

from db import database
from api.models.chapter import ChapterModel
from api.models.course import CourseModel
from utils.sorting import sort, Sort_by

router = APIRouter()

@router.get(
        "/",
        response_model=List[CourseModel],
        response_description="""List of all available courses with support to sort data by title, date & rating (descending).
            And optional filtering of courses based on domain."""
    )
async def get_courses(
        request: Request,
        sort_mode: Sort_by = Query(Sort_by.TITLE, description="Sorting Course by Name, Date, Course Rating"),
        domain: Optional[str] = Query(None, description="Filter courses by domain")
    )-> list[CourseModel]:

    query = {}

    if domain:
        query["domain"] = domain

    # Fetch courses from MongoDB based on the query
    courses = await database.get_all(database.Collections.COURSE, request, query)
    courses = sort(courses, sort_mode)
    courses = [CourseModel(**course) for course in courses]

    return courses

@router.get(
        "/{course_id}",
        response_model=CourseModel,
        response_description="Get the course overview by course_id"
    )
async def get_course(
        request: Request,
        course_id: str
    ) -> CourseModel:

    course = await database.get_by_id(database.Collections.COURSE, course_id, request)

    if course:
        return CourseModel(**course)
    raise HTTPException(status_code=404, detail="Course not found")

@router.get(
        "/{course_id}/chapters/{chapter_id}",
        response_model=ChapterModel,
        response_description="Get specific chapter information, by using course_id and chapter_id"
    )
async def get_chapter(
        request: Request,
        course_id: str,
        chapter_id: str
    ) -> ChapterModel:
    
    course = await database.get_by_id(database.Collections.COURSE, course_id, request)
    chapter = await database.get_by_id(database.Collections.CHAPTER, chapter_id, request)
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return ChapterModel(**chapter)

@router.post(
        "/{course_id}/chapters/{chapter_id}/rate",
        response_description="Allow users to rate each chapters, rating between 0 to 5"
    )
async def rate_chapter(
        request: Request,
        course_id: str,
        chapter_id: str,
        rating: float = Form(..., ge=0, le=5)
    ):

    course = await database.get_by_id(database.Collections.COURSE, course_id, request)
    chapter = await database.get_by_id(database.Collections.CHAPTER, chapter_id, request)
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    await database.update_by_id(database.Collections.CHAPTER, request, {"$push": {"user_ratings": rating}}, chapter["_id"])
    
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Chapter rated successfully"})
        
