import os
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from dotenv import load_dotenv

from .models import Email, ScanResult, User
from .serializers import EmailSerializer, ScanResultSerializer, UserSerializer
from mocks.email_generator import generate_mock_email, generate_mock_scan_result

load_dotenv()  # loads api/.env when running locally inside container
MAIL_SERVICE_URL = os.getenv("MAIL_SERVICE_URL")
AI_SERVICE_URL = os.getenv("AI_SERVICE_URL")

@api_view(['POST'])
def submit_email(request):
    """
    Endpoint receives a trigger/payload (mailserver or manual), tries to fetch full email
    from MAIL_SERVICE_URL, if not available uses mock. Then tries to call AI scanner,
    falls back to mock. Response includes 'message' describing which services were mocked.
    """
    message_parts = []
    email_data = None

    # 1) Get email data (mail server service)
    try:
        if MAIL_SERVICE_URL:
            resp = requests.post(MAIL_SERVICE_URL, json=request.data, timeout=5)
            resp.raise_for_status()
            email_data = resp.json()
        else:
            raise RuntimeError("MAIL_SERVICE_URL not set")
    except Exception as e:
        message_parts.append(f"Mail service not available, using mock: {str(e)}")
        email_data = generate_mock_email()

    # Map sender/recipient to Users (create if missing)
    sender_obj, _ = User.objects.get_or_create(email=email_data['sender'], defaults={'name': 'Unknown'})
    recipient_obj, _ = User.objects.get_or_create(email=email_data['recipient'], defaults={'name': 'Unknown'})

    # Create email record
    received_at = email_data.get('received_at')
    try:
        email = Email.objects.create(
            sender=sender_obj,
            recipient=recipient_obj,
            subject=email_data.get('subject', '')[:255],
            body=email_data.get('body', ''),
            attachments=email_data.get('attachments', []),
            received_at=received_at if received_at else timezone.now()
        )
    except Exception as e:
        return Response({"error": "Failed to save email", "detail": str(e)}, status=500)

    # 2) Try AI scanner
    try:
        if AI_SERVICE_URL:
            scan_resp = requests.post(AI_SERVICE_URL, json={"subject": email.subject, "body": email.body}, timeout=5)
            scan_resp.raise_for_status()
            result_data = scan_resp.json()
            result = result_data.get('result', 'safe')
            confidence = float(result_data.get('confidence', 0.0))
        else:
            raise RuntimeError("AI_SERVICE_URL not set")
    except Exception as e:
        message_parts.append(f"AI scan service not available, using mock: {str(e)}")
        result, confidence = generate_mock_scan_result()

    # Create scan result
    try:
        scan_result = ScanResult.objects.create(
            email=email,
            result=result,
            confidence=confidence,
            scanned_at=timezone.now()
        )
    except Exception as e:
        return Response({"error": "Failed to save scan result", "detail": str(e)}, status=500)

    message = " | ".join(message_parts) if message_parts else "All services OK"
    return Response({
        "message": message,
        "email": EmailSerializer(email).data,
        "scan_result": ScanResultSerializer(scan_result).data
    })


@api_view(['GET'])
def list_scans(request):
    scans = ScanResult.objects.all().order_by('-scanned_at')
    serializer = ScanResultSerializer(scans, many=True)
    return Response(serializer.data)


# User admin endpoints
@api_view(['GET','POST'])
def users_list_create(request):
    if request.method == 'GET':
        users = User.objects.all()
        return Response(UserSerializer(users, many=True).data)
    # POST -> create
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        return Response(UserSerializer(instance).data, status=201)
    return Response(serializer.errors, status=400)
