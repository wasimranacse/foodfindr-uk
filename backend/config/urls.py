from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def health_check(_request):
    return JsonResponse({"status": "ok", "service": "foodfindr-api"})


api_v1_patterns = [
    path("health/", health_check, name="api-health"),
    path("auth/", include("apps.users.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.users.urls")),
    path("api/v1/", include((api_v1_patterns, "api"), namespace="v1")),
]
