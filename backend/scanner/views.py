from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Import the emails app contract
from emails.mock_service import mock_service
from emails.models import ScanLog

from .service_selector import try_real_scan
import logging
logger = logging.getLogger(__name__)

# class ScanView(APIView):
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     def post(self, request):
#         email_content = {
#             "from": request.data.get("from"),
#             "subject": request.data.get("subject"),
#             "body": request.data.get("body"),
#         }

#         # 🔥 CALL THE EMAILS SERVICE HERE
#         scan_result = mock_service.scan_email(email_content["body"])

#         # Save in DB
#         log = ScanLog.objects.create(
#             sender=email_content["from"],
#             subject=email_content["subject"],
#             body=email_content["body"],
#             result="malicious" if scan_result["malicious"] else "safe",
#             confidence=scan_result["confidence"],
#         )

#         return Response({
#             "id": log.id,
#             "result": log.result,
#             "confidence": log.confidence,
#         })

class ScanView(APIView):
    def post(self, request):
        body = request.data.get("body", "")

        logger.info("Received scan request")

        # 🔥 dynamic real OR mock call
        scan_result = try_real_scan(body)

        log = ScanLog.objects.create(
            sender=request.data.get("from"),
            subject=request.data.get("subject"),
            body=body,
            result="malicious" if scan_result["malicious"] else "safe",
            confidence=scan_result["confidence"]
        )

        logger.info(f"Scan result: {scan_result}")

        return Response({
            "id": log.id,
            "result": log.result,
            "confidence": log.confidence,
            "used": "real" if "real" in scan_result else "mock"
        })


class LogsView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        logs = ScanLog.objects.order_by("-scanned_at")[:200]

        return Response([
            {
                "id": log.id,
                "sender": log.sender,
                "subject": log.subject,
                "result": log.result,
                "confidence": log.confidence,
                "scanned_at": log.scanned_at,
            }
            for log in logs
        ])
