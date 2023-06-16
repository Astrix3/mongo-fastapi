from fastapi.testclient import TestClient
from main import app

from tests.sample_data import sample_course_1, sample_course_2
from tests.database_mock import *

# Create a MongoDB test client
client = TestClient(app)

def test_get_courses(mock_get_all):
    # Send GET request to /courses endpoint
    response = client.get("/courses")
    assert response.status_code == 200

    # Verify the response contains the sample course
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == sample_course_1.name
    assert response.json()[1]["name"] == sample_course_2.name
    mock_get_all.assert_called_once()


def test_get_course(mock_get_one_course):
    # Send GET request to /courses/{course_id} endpoint
    response = client.get(f"/courses/{sample_course_1.get('_id')}")
    assert response.status_code == 200

    # Verify the response contains the sample course
    assert response.json()["name"] == sample_course_1.name
    mock_get_one_course.assert_called_once()


def test_get_chapter(mock_get_one_chapter):
    # Send GET request to /courses/{course_id}/chapters/{chapter_id} endpoint
    response = client.get(f"/courses/{sample_course_1.get('_id')}/chapters/{sample_course_1.get('chapters')[0].get('_id')}")
    assert response.status_code == 200

    # Verify the response contains the sample chapter
    assert response.json()["name"] == sample_course_1.chapters[0].name
    mock_get_one_chapter.assert_called_once()


def test_rate_chapter():
    # Send POST request to /courses/{course_id}/chapters/{chapter_id}/rate endpoint
    response = client.post(f"/courses/{sample_course_1.get('_id')}/chapters/{sample_course_1.get('chapters')[0].get('_id')}/rate", data={"rating": 4.5})
    assert response.status_code == 201

    # Verify the response message
    assert response.json()["message"] == "Chapter rated successfully"
    mock_update_one_chapter.assert_called_once()
