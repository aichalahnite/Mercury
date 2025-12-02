from django.urls import path
from .views import ScanView, LogsView

urlpatterns = [
    path("scan/", ScanView.as_view(), name="scan"),
    path("logs/", LogsView.as_view(), name="logs"),
]
