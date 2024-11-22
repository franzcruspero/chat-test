import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model


@pytest.mark.django_db
class TestJWTEndpoints:
    def test_token_obtain(self, api_client):
        User = get_user_model()
        _ = User.objects.create_user(username="testuser", password="testpass123")

        url = reverse("v1:token_obtain_pair")
        response = api_client.post(
            url, {"username": "testuser", "password": "testpass123"}
        )

        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

    def test_token_refresh(self, api_client):
        User = get_user_model()
        _ = User.objects.create_user(username="testuser", password="testpass123")

        obtain_url = reverse("v1:token_obtain_pair")
        obtain_response = api_client.post(
            obtain_url, {"username": "testuser", "password": "testpass123"}
        )

        refresh_url = reverse("v1:token_refresh")
        refresh_response = api_client.post(
            refresh_url, {"refresh": obtain_response.data["refresh"]}
        )

        assert refresh_response.status_code == 200
        assert "access" in refresh_response.data
