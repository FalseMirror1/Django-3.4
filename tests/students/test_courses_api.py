import pytest as pytest
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_get_a_course(client, course_factory):
    """проверка получения 1го курса"""
    create = course_factory(_quantity=1)
    first_course = create[0]
    response = client.get(f'/api/v1/courses/{first_course.id}/')
    assert response.status_code == 200

    data = response.json()
    assert data['name'] == first_course.name


@pytest.mark.django_db
def test_get_list_of_courses(client, course_factory):
    """проверка получения списка курса"""
    create = course_factory(_quantity=50)
    response = client.get('/api/v1/courses/')
    assert response.status_code == 200

    data = response.json()
    for i, course in enumerate(data):
        assert course['name'] == create[i].name


@pytest.mark.django_db
def test_id_filtering(client, course_factory):
    """проверка фильтрации списка курсов по id"""
    create = course_factory(_quantity=1)
    response = client.get('/api/v1/courses/', {'id': create[0].id})
    assert response.status_code == 200

    data = response.json()
    assert data[0]['id'] == create[0].id


@pytest.mark.django_db
def test_name_filtering(client, course_factory):
    """проверка фильтрации списка курсов по name"""
    create = course_factory(_quantity=1)
    response = client.get('/api/v1/courses/', {'name': create[0].name})
    assert response.status_code == 200

    data = response.json()
    assert data[0]['name'] == create[0].name


@pytest.mark.django_db
def test_course_creating(client):
    """тест успешного создания курса"""
    url = reverse('courses-list')
    data = {
        'name': 'test'
    }
    response = client.post(url, data)
    assert response.status_code == 201
    assert response.data["name"] == data["name"]


@pytest.mark.django_db
def test_course_updating(client, course_factory):
    """тест успешного обновления курса"""
    create = course_factory(_quantity=10)
    url = reverse('courses-detail', args=[create[0].id, ])
    upd_data = {
        'name': 'new name'
    }
    response = client.patch(url, upd_data)
    assert response.status_code == 200

    data = response.json()
    assert data['name'] == upd_data['name']


@pytest.mark.django_db
def test_course_deleting(client, course_factory):
    """тест успешного удаления курса"""
    create = course_factory(_quantity=1)
    url = reverse('courses-detail', args=[create[0].id, ])
    response = client.delete(url)
    assert response.status_code == 204


