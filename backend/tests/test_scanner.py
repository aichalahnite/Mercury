from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from scanner.models import ScanLog

User = get_user_model()

def auth_client():
    u = User.objects.create_user("u", "u@u.com", "pass")
    c = APIClient()
    tok = c.post("/auth/token/", {"username": "u", "password": "pass"}).data["access"]
    c.credentials(HTTP_AUTHORIZATION="Bearer " + tok)
    return c

def test_scan_creates_log():
    client = auth_client()

    payload = {
        "from": "x@test.com",
        "subject": "Hello",
        "body": "Hello world"
    }

    res = client.post("/scanner/scan/", payload)

    assert res.status_code == 200
    assert ScanLog.objects.count() == 1
    assert "result" in res.data

def test_logs_list():
    client = auth_client()

    # create a log
    client.post("/scanner/scan/", {"from": "x", "subject": "y", "body": "z"})

    res = client.get("/scanner/logs/")

    assert res.status_code == 200
    assert len(res.data) >= 1
