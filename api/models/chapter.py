from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_computed import computed, Computed

class ChapterModel(BaseModel):
    chapter_id: str = Field(alias="_id")
    course_id: str = Field(..., title="Course ID")
    name: str = Field(..., description="Title for Chapter", title="Title")
    content: str = Field(..., alias="text",description="Contents of the chapter", title="Content")
    user_ratings: Optional[List[float]] = Field([], description="List of the user rating for chapter", title="Chapter Ratings")
    rating: Computed[float]

    @computed('rating')
    def rating(user_ratings, **kwargs) -> float:
        """
            Calculate the overall rating for the course based on the chapter ratings.
        """
        if not user_ratings:
            return None

        total_rating = sum(rating for rating in user_ratings)
        total_rated_chapters = len(user_ratings)
        return total_rating / total_rated_chapters

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "chapter_id": "0000123-0000-0000-0000-0000000a0f",
            "course_id": "0000222-0000-0000-0000-000000ba0f",
            "name":"This is CS50x 2022, now in 4K HDR",
            "content":"Introduction to Programming",
            "user_ratings": [4.1, 2.0],
            "rating": 2.4
        }