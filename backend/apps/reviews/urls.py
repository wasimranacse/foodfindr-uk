from django.urls import path

from .views import CustomerReviewUpdateDeleteView, RestaurantReviewListCreateView

urlpatterns = [
    path("restaurants/<int:restaurant_id>/reviews/", RestaurantReviewListCreateView.as_view(), name="restaurant-reviews"),
    path("reviews/<int:pk>/", CustomerReviewUpdateDeleteView.as_view(), name="customer-review-detail"),
]
