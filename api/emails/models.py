from django.db import models
from django.contrib.auth.models import AbstractUser

class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=50, choices=[('admin','Admin'),('user','User')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Email(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sent_emails')
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='received_emails')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    attachments = models.JSONField(default=list)  # list of dicts: {"filename":..., "size":...}
    received_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} from {self.sender}"

class ScanResult(models.Model):
    email = models.OneToOneField(Email, on_delete=models.CASCADE, related_name='scan_result')
    result = models.CharField(max_length=20, choices=[('safe','Safe'),('suspicious','Suspicious'),('malicious','Malicious')])
    confidence = models.FloatField()
    scanned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.result} ({self.confidence})"
