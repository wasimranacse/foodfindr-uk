from django.urls import path

from .views import (
    OwnerMenuCategoryCreateView,
    OwnerMenuCategoryUpdateDeleteView,
    OwnerMenuItemCreateView,
    OwnerMenuItemUpdateDeleteView,
    RestaurantMenuView,
)

urlpatterns = [
    path("restaurants/<int:restaurant_id>/menu/", RestaurantMenuView.as_view(), name="restaurant-menu"),
    path("owner/menu-categories/", OwnerMenuCategoryCreateView.as_view(), name="owner-menu-category-create"),
    path("owner/menu-categories/<int:pk>/", OwnerMenuCategoryUpdateDeleteView.as_view(), name="owner-menu-category-detail"),
    path("owner/menu-items/", OwnerMenuItemCreateView.as_view(), name="owner-menu-item-create"),
    path("owner/menu-items/<int:pk>/", OwnerMenuItemUpdateDeleteView.as_view(), name="owner-menu-item-detail"),
]
