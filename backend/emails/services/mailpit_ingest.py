import requests
from emails.models import Email
from scanner.service_selector import try_real_scan
from scanner.models import ScanLog
from django.contrib.auth import get_user_model

User = get_user_model()

MAILPIT_API = "http://mailpit:8025/api/v1/messages"

def ingest_mailpit():
    res = requests.get(MAILPIT_API).json()

    for msg in res["messages"]:
        full = requests.get(
            f"http://mailpit:8025/api/v1/message/{msg['ID']}"
        ).json()

        to = full["To"][0]["Address"]
        user = User.objects.filter(email=to).first()
        if not user:
            continue

        body = full["Text"]

        email = Email.objects.create(
            user=user,
            sender=full["From"]["Address"],
            recipient=to,
            subject=full["Subject"],
            body=body,
            folder="inbox",
            is_outgoing=False,
        )

        scan = try_real_scan(body)

        ScanLog.objects.create(
            email=email,
            user=user,
            result="malicious" if scan["malicious"] else "safe",
            confidence=scan["confidence"],
        )
