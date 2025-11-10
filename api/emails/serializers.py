from rest_framework import serializers
from .models import User, Email, ScanResult

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'role', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']

class EmailSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    recipient = UserSerializer()

    class Meta:
        model = Email
        fields = ['id', 'sender', 'recipient', 'subject', 'body', 'attachments', 'received_at', 'processed']
        read_only_fields = ['id', 'received_at', 'processed']

class ScanResultSerializer(serializers.ModelSerializer):
    email = EmailSerializer()

    class Meta:
        model = ScanResult
        fields = ['id', 'email', 'result', 'confidence', 'scanned_at']
        read_only_fields = ['id', 'scanned_at']
