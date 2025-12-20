from django.urls import path
from .views import SendEmailMock, ScanEmailMock, SendEmailView

urlpatterns = [
    path("mock/send/", SendEmailMock.as_view()),
    path("mock/scan/", ScanEmailMock.as_view()),
    path("send/", SendEmailView.as_view()),
]
