import pytest
from tests.sample_data import sample_course_1, sample_chapter_1, sample_course_2

@pytest.fixture
def mock_get_all(mocker):
    mocker.patch("api.endpoints.course.database.get_all", return_value=[sample_course_1, sample_course_2])
    return mocker

@pytest.fixture
def mock_get_one_course(mocker):
    mocker.patch("api.endpoints.course.database.get_by_id", return_value=sample_course_1)
    return mocker

@pytest.fixture
def mock_get_one_chapter(mocker):
    mocker.patch("api.endpoints.course.database.get_by_id", return_value=sample_chapter_1)
    return mocker

@pytest.fixture
def mock_update_one_chapter(mocker):
    mocker.patch("api.endpoints.course.database.update_by_id", return_value=None)
    return mocker
