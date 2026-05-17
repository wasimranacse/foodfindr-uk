from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def health_check(_request):
    return JsonResponse({"status": "ok", "service": "foodfindr-api"})


api_v1_patterns = [
    path("health/", health_check, name="api-health"),
    path("auth/", include("apps.users.urls")),
    path("", include("apps.locations.urls")),
    path("", include("apps.restaurants.urls")),
    path("", include("apps.menus.urls")),
    path("", include("apps.offers.urls")),
    path("", include("apps.reviews.urls")),
    path("", include("apps.favourites.urls")),
    path("", include("apps.analytics.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.users.urls")),
    path("api/", include("apps.locations.urls")),
    path("api/", include("apps.restaurants.urls")),
    path("api/", include("apps.menus.urls")),
    path("api/", include("apps.offers.urls")),
    path("api/", include("apps.reviews.urls")),
    path("api/", include("apps.favourites.urls")),
    path("api/", include("apps.analytics.urls")),
    path("api/v1/", include((api_v1_patterns, "api"), namespace="v1")),
]
