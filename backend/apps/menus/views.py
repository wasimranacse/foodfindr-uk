from rest_framework import generics, permissions

from apps.restaurants.models import Restaurant
from apps.users.permissions import IsRestaurantOwner, IsVerifiedUser

from .models import MenuCategory, MenuItem
from .serializers import MenuCategorySerializer, MenuItemSerializer


class RestaurantMenuView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = MenuCategorySerializer

    def get_queryset(self):
        restaurant_id = self.kwargs["restaurant_id"]
        return (
            MenuCategory.objects.filter(
                restaurant_id=restaurant_id,
                restaurant__is_approved=True,
                is_active=True,
            )
            .prefetch_related("items")
            .order_by("display_order", "name")
        )


class OwnerMenuCategoryCreateView(generics.CreateAPIView):
    serializer_class = MenuCategorySerializer
    permission_classes = [IsRestaurantOwner]


class OwnerMenuCategoryUpdateDeleteView(generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = MenuCategorySerializer
    permission_classes = [IsRestaurantOwner]
    http_method_names = ["patch", "delete"]

    def get_queryset(self):
        if self.request.user.role == "super_admin":
            return MenuCategory.objects.all()
        return MenuCategory.objects.filter(restaurant__owner=self.request.user)


class OwnerMenuItemCreateView(generics.CreateAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [IsRestaurantOwner]


class OwnerMenuItemUpdateDeleteView(generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [IsRestaurantOwner]
    http_method_names = ["patch", "delete"]

    def get_queryset(self):
        if self.request.user.role == "super_admin":
            return MenuItem.objects.all()
        return MenuItem.objects.filter(restaurant__owner=self.request.user)
