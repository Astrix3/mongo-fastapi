from enum import Enum
from typing import List

class Sort_by(str, Enum):
    TITLE = "name"
    DATE = "date"
    RATING = "rating"


def sort(data: list, mode: Sort_by) -> List:
    print("Sort mode", mode)
    print(data)
    if mode == Sort_by.TITLE:
        data.sort(key=lambda course: course.get("name", 0))
    elif mode == Sort_by.DATE:
        data.sort(key=lambda course: course.get("date", 0), reverse=True)
    elif mode == Sort_by.RATING:
        data.sort(key=lambda course: course.get("rating", 0), reverse=True)
    
    return data    