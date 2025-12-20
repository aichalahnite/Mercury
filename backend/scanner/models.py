from django.conf import settings
from django.db import models

class ScanLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    sender = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()
    result = models.CharField(max_length=50)
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.subject} ({self.result})"
