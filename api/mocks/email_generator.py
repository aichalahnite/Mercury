import random
from datetime import datetime
from faker import Faker

fake = Faker()

def generate_mock_email():
    return {
        "sender": fake.email(),
        "recipient": fake.email(),
        "subject": fake.sentence(nb_words=6),
        "body": fake.paragraph(nb_sentences=3),
        "attachments": [
            {"filename": fake.file_name(extension='pdf'), "size": random.randint(1000, 1000000)}
            for _ in range(random.randint(0, 2))
        ],
        "received_at": datetime.now().isoformat(),
    }

def generate_mock_scan_result():
    choices = [("safe", 0.95), ("suspicious", 0.85), ("malicious", 0.99)]
    return random.choice(choices)
