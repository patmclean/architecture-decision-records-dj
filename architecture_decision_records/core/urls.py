"""ADR URL Configuration."""

from django.contrib import admin
from django.urls import path, include

# from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("architecture_decision_records.decisions.urls")),
]
