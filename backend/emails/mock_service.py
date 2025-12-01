import random
from .interfaces import EmailServiceInterface

class MockEmailService(EmailServiceInterface):
    def send_email(self, to, subject, body):
        return {
            "id": random.randint(1000,9999),
            "to": to,
            "subject": subject,
            "status": "sent_mock"
        }

    def scan_email(self, content):
        return {
            "scan_id": random.randint(1,9999),
            "malicious": random.choice([True, False]),
            "confidence": round(random.random(),2)
        }

mock_service = MockEmailService()
