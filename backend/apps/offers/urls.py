from django.urls import path

from .views import ActiveOfferListView, OwnerOfferCreateView, OwnerOfferUpdateDeleteView, RestaurantOfferListView

urlpatterns = [
    path("offers/active/", ActiveOfferListView.as_view(), name="offer-active-list"),
    path("restaurants/<int:restaurant_id>/offers/", RestaurantOfferListView.as_view(), name="restaurant-offers"),
    path("owner/offers/", OwnerOfferCreateView.as_view(), name="owner-offer-create"),
    path("owner/offers/<int:pk>/", OwnerOfferUpdateDeleteView.as_view(), name="owner-offer-detail"),
]
