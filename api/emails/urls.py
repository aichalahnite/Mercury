from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import views

schema_view = get_schema_view(
    openapi.Info(title="Mercury Backend API", default_version='v1', description="Stable API contract for Mercury backend"),
    public=True, permission_classes=(permissions.AllowAny,)
)

urlpatterns = [
    path('submit_email/', views.submit_email, name='submit_email'),
    path('list_scans/', views.list_scans, name='list_scans'),
    path('users/', views.users_list_create, name='users'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
