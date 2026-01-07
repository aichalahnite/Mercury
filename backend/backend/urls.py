from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from django.contrib.auth import views as auth_views
from users.views import signup

from graphene_django.views import GraphQLView

from django.conf import settings
from backend.schema import schema  # ✅ IMPORT SCHEMA


schema_view = get_schema_view(
    openapi.Info(title="Mock Backend API", default_version="v1"),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("admin/", admin.site.urls),

    # Auth
    path("auth/token/", TokenObtainPairView.as_view()),
    path("auth/token/refresh/", TokenRefreshView.as_view()),

    # Apps
    path("users/", include("users.urls")),
    path("emails/", include("emails.urls")),
    path("scanner/", include("scanner.urls")),

    # Swagger
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0)),

    # Auth pages
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html")),
    path("logout/", auth_views.LogoutView.as_view()),
    path("signup/", signup),

    # ✅ GraphQL endpoint
    path(
        "graphql/",
        csrf_exempt(
            GraphQLView.as_view(
                schema=schema,
                graphiql=settings.DEBUG,  # ✅ DEV ONLY
            )
        ),
    ),
]
