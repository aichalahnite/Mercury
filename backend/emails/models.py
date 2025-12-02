from django.db import models

class ScanLog(models.Model):
    sender = models.CharField(max_length=255, null=True, blank=True)
    subject = models.CharField(max_length=255, null=True, blank=True)
    body = models.TextField(null=True, blank=True)

    result = models.CharField(max_length=50)  # "safe" / "malicious"
    confidence = models.FloatField(default=0.0)

    scanned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} - {self.subject} ({self.result})"

