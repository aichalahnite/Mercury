from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .mock_service import mock_service
from .models import Email
from scanner.service_selector import try_real_send_email


class SendEmailMock(APIView):
    """
    Admin-only mock email sender
    """
    permission_classes = [IsAdminUser]

    def post(self, request):
        data = mock_service.send_email(
            to=request.data.get("to", "test@example.com"),
            subject=request.data.get("subject", "Mock Email"),
            body=request.data.get("body", "")
        )
        return Response(data)


class ScanEmailMock(APIView):
    """
    Admin-only mock email scanner
    """
    permission_classes = [IsAdminUser]

    def post(self, request):
        data = mock_service.scan_email(
            request.data.get("content", "Test content")
        )
        return Response(data)


class SendEmailView(APIView):
    """
    Authenticated REST endpoint for sending emails
    Used by frontend if NOT using GraphQL
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        to = request.data.get("to")
        subject = request.data.get("subject")
        body = request.data.get("body")

        if not to or not subject or not body:
            return Response(
                {"error": "to, subject and body are required"},
                status=400
            )

        route = getattr(request, "service_route", {}).get("mailserver", "mock")

        if route == "real":
            try_real_send_email({
                "to": to,
                "subject": subject,
                "body": body,
            })
        else:
            mock_service.send_email(to, subject, body)

        email = Email.objects.create(
            user=user,
            sender=user.email,
            recipient=to,
            subject=subject,
            body=body,
            folder="sent",
            is_outgoing=True,
        )

        return Response({
            "status": "sent",
            "used": route,
            "email_id": email.id,
        })
