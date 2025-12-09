from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

def auth_client():
    user = User.objects.create_user("test", "test@example.com", "pass")
    client = APIClient()
    res = client.post("/auth/token/", {"username": "test", "password": "pass"})
    client.credentials(HTTP_AUTHORIZATION="Bearer " + res.data["access"])
    return client

def test_mock_send_email():
    client = auth_client()

    payload = {
        "to": "a@b.com",
        "subject": "Hi",
        "body": "Test"
    }

    res = client.post("/emails/mock/send/", payload)

    assert res.status_code == 200
    assert "status" in res.data
    assert res.data["status"] == "sent_mock"
