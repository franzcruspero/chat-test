import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestCustomPasswordChangeSerializer:
    def test_password_change_incorrect_old_password(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse("v1:rest_password_change")

        data = {
            "old_password": "wrong_password",
            "new_password1": "NewPassword123!",
            "new_password2": "NewPassword123!",
        }

        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get("old_password")[0] == "Incorrect password. Try again."

    def test_password_change_success(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse("v1:rest_password_change")

        data = {
            "old_password": "password",
            "new_password1": "NewPassword123!",
            "new_password2": "NewPassword123!",
        }

        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_200_OK

    def test_password_change_incorrect_new_password1(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse("v1:rest_password_change")

        data = {
            "old_password": "password",
            "new_password1": "NewPassword1234!",
            "new_password2": "NewPassword123!",
        }

        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get("new_password2")[0] == "Passwords do not match."

    def test_password_change_new_password_same_as_old_password(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse("v1:rest_password_change")

        data = {
            "old_password": "password",
            "new_password1": "password",
            "new_password2": "password",
        }

        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.data.get("new_password1")[0]
            == "New password cannot be the same as current password."
        )

    def test_password_change_password_length(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse("v1:rest_password_change")

        data = {
            "old_password": "password",
            "new_password1": "test",
            "new_password2": "test",
        }

        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get("new_password1")[0] == "Must be at least 8 characters."
