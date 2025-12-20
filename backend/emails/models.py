from django.conf import settings
from django.db import models


class Email(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="emails"
    )

    sender = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()

    is_outgoing = models.BooleanField(default=False)
    has_attachments = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} → {self.user.username}"
