from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .mock_service import mock_service

class SendEmailMock(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = mock_service.send_email(
            to=request.data.get("to","test@example.com"),
            subject=request.data.get("subject","Mock Email"),
            body=request.data.get("body","")
        )
        return Response(data)

class ScanEmailMock(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = mock_service.scan_email(
            request.data.get("content","Test content")
        )
        return Response(data)
