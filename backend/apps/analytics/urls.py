from django.urls import path

from .views import AnalyticsEventCreateView, OwnerRestaurantAnalyticsView

urlpatterns = [
    path("analytics/event/", AnalyticsEventCreateView.as_view(), name="analytics-event-create"),
    path(
        "owner/restaurants/<int:restaurant_id>/analytics/",
        OwnerRestaurantAnalyticsView.as_view(),
        name="owner-restaurant-analytics",
    ),
]
