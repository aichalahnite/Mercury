from django.urls import path
from .views import SendEmailMock, ScanEmailMock, SendEmailView

urlpatterns = [
    #These remain admin-only.
    path("mock/send/", SendEmailMock.as_view()),
    path("mock/scan/", ScanEmailMock.as_view()),
]
