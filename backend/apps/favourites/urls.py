from django.urls import path

from .views import CustomerFavouriteDeleteView, CustomerFavouriteListCreateView

urlpatterns = [
    path("customer/favourites/", CustomerFavouriteListCreateView.as_view(), name="customer-favourite-list"),
    path("customer/favourites/<int:pk>/", CustomerFavouriteDeleteView.as_view(), name="customer-favourite-detail"),
]
