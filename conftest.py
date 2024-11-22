import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from pytest_factoryboy import register
from rest_framework.test import APIClient
from users.tests.factories import UserFactory

register(UserFactory)


@pytest.fixture
def api_client():
    api_client = APIClient()
    yield api_client


@pytest.fixture
def authenticated_api_client(api_client, user):
    api_client.force_authenticate(user=user)
    yield api_client


@pytest.fixture
def admin_client(client, admin_user):
    client.force_login(admin_user)
    yield client


@pytest.fixture
def single_attachment():
    return SimpleUploadedFile(
        "test_attachment.txt",
        b"This is a test attachment content",
        content_type="text/plain",
    )


@pytest.fixture
def multiple_attachments():
    return [
        SimpleUploadedFile(
            "attachment1.txt",
            b"Content of attachment 1",
            content_type="text/plain",
        ),
        SimpleUploadedFile(
            "attachment2.pdf",
            b"Content of attachment 2",
            content_type="application/pdf",
        ),
        ("attachment3.csv", b"Content of attachment 3", "text/csv"),
    ]
