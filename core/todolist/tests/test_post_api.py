from rest_framework.test import APIClient
from django.urls import reverse
import pytest
from datetime import datetime
from accounts.models import User


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def common_user():
    user = User.objects.create_user(
        email="admin@admin.com", password="123", is_verified=True
    )
    return user


@pytest.mark.django_db
class TestTasktApi:
    def test_get_task_response_200_status(self, api_client):
        url = reverse("todolist:api-v1:task-list")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_task_response_403_status(self, api_client):
        url = reverse("todolist:api-v1:task-list")
        data = {
            "title": "test",
            "created_date": datetime.now(),
        }
        response = api_client.post(url, data)
        assert response.status_code == 403


    def test_create_task_response_201_status(self, api_client, common_user):
        url = reverse("todolist:api-v1:task-list")
        data = {
            "title": "test",
         
             "created_date": datetime.now(),
        }
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.post(url, data)
        assert response.status_code == 201

    def test_create_task_invalid_data_response_400_status(
        self, api_client, common_user
    ):
        url = reverse("todolist:api-v1:task-list")
        data = {"invalid": "test" }
        user = common_user

        api_client.force_authenticate(user=user)
        response = api_client.post(url, data)
        assert response.status_code == 400
