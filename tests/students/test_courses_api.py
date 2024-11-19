import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from students.models import Course


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(**kwargs):
        return baker.make(Course, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    def factory(**kwargs):
        return baker.make('students.Student', **kwargs)
    return factory


@pytest.mark.django_db
def test_retrieve_course(api_client, course_factory):
    course = course_factory(name="Test Course")
    url = f"/api/v1/courses/{course.id}/"
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['name'] == "Test Course"


@pytest.mark.django_db
def test_list_courses(api_client, course_factory):
    course_factory(name="Course 1")
    course_factory(name="Course 2")
    response = api_client.get("/api/v1/courses/")
    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_filter_courses_by_id(api_client, course_factory):
    course1 = course_factory(name="Course 1", id=1)
    course_factory(name="Course 2", id=2)
    response = api_client.get("/api/v1/courses/", data={'id': course1.id})
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['id'] == course1.id


@pytest.mark.django_db
def test_filter_courses_by_name(api_client, course_factory):
    course_factory(name="Course 1")
    course2 = course_factory(name="Course 2")
    response = api_client.get("/api/v1/courses/", data={'name': course2.name})
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['name'] == course2.name


@pytest.mark.django_db
def test_create_course(api_client):
    data = {'name': 'New Course'}
    response = api_client.post("/api/v1/courses/", data=data, format='json')
    assert response.status_code == 201
    assert response.data['name'] == 'New Course'


@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    course = course_factory(name="Old Course")
    data = {'name': 'Updated Course'}
    url = f"/api/v1/courses/{course.id}/"
    response = api_client.patch(url, data=data, format='json')
    assert response.status_code == 200
    assert response.data['name'] == 'Updated Course'


@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    course = course_factory()
    url = f"/api/v1/courses/{course.id}/"
    response = api_client.delete(url)
    assert response.status_code == 204
