from django.urls import path

from .views import (
    AdminRestaurantApprovalView,
    FeaturedRestaurantView,
    NearbyRestaurantView,
    OwnerRestaurantCreateView,
    OwnerRestaurantUpdateView,
    RestaurantDetailView,
    RestaurantListView,
    RestaurantOffersView,
    TopRatedRestaurantView,
)

urlpatterns = [
    path("restaurants/", RestaurantListView.as_view(), name="restaurant-list"),
    path("restaurants/nearby/", NearbyRestaurantView.as_view(), name="restaurant-nearby"),
    path("restaurants/top-rated/", TopRatedRestaurantView.as_view(), name="restaurant-top-rated"),
    path("restaurants/featured/", FeaturedRestaurantView.as_view(), name="restaurant-featured"),
    path("restaurants/offers/", RestaurantOffersView.as_view(), name="restaurant-with-offers"),
    path("restaurants/<slug:slug>/", RestaurantDetailView.as_view(), name="restaurant-detail"),
    path("owner/restaurants/", OwnerRestaurantCreateView.as_view(), name="owner-restaurant-create"),
    path("owner/restaurants/<int:pk>/", OwnerRestaurantUpdateView.as_view(), name="owner-restaurant-update"),
    path(
        "admin/restaurants/<int:pk>/<str:action>/",
        AdminRestaurantApprovalView.as_view(),
        name="admin-restaurant-approval",
    ),
]
