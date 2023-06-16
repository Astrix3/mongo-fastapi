from datetime import datetime
from pydantic import BaseModel, Field
from pydantic_computed import computed, Computed
from typing import List

from api.models.chapter import ChapterModel

class CourseModel(BaseModel):
    course_id: str = Field(alias="_id")
    name: str = Field(..., description="Title for the course", title="Course Name")
    date: int  = Field(..., description="Creation date as a unix timestamp", title="Course Name")
    description: str = Field(..., description="Description of the course", title="Course Description")
    domain: list = Field(..., description="List of the course domain(s)")
    chapters: List[ChapterModel] = Field([], description="List of the course chapters. Each chapter has a title name and contents text", title="Course Chapters")
    created_at: Computed[datetime]
    rating: Computed[float]

    @computed('created_at')
    def compute_created_at(date, **kwargs) -> datetime:
        """
            The datetime object representing course creation time.
        """
        return datetime.fromtimestamp(date)

    @computed('rating')
    def overall_rating(chapters, **kwargs) -> float:
        """
            Calculate the overall rating for the course based on the chapter ratings.
        """
        if not chapters:
            return None

        total_rating = sum(chapter.rating for chapter in chapters if chapter.rating is not None)
        total_rated_chapters = sum(1 for chapter in chapters if chapter.rating is not None)
        return format((total_rating / total_rated_chapters), ".2f")

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
                "course_id": "0000222-0000-0000-0000-000000ba0f",
                "name":"Highlights of Calculus",
                "date":1530133200,
                "description":"Highlights of Calculus is a series of short videos that introduces the basic ideas of calculus \u2014 how it works and why it is important. The intended audience is high school students, college students, or anyone who might need help understanding the subject.\nIn addition to the videos, there are summary slides and practice problems complete with an audio narration by Professor Strang. You can find these resources to the right of each video.",
                "domain":[
                    "mathematics"
                ],
                "chapters": [
                    {
                        "chapter_id": "0000123-0000-0000-0000-0000000a0f",
                        "course_id": "0000222-0000-0000-0000-000000ba0f",
                        "name":"This is CS50x 2022, now in 4K HDR",
                        "content":"Introduction to Programming",
                        "user_ratings": [4.1, 2.0],
                        "rating": 2.4
                    }
                ],
                "created_at": "",
                "overall_rating": 4.5
        }