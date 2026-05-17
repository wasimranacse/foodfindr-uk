from rest_framework import generics

from apps.users.permissions import IsCustomer

from .models import FavouriteRestaurant
from .serializers import FavouriteRestaurantSerializer


class CustomerFavouriteListCreateView(generics.ListCreateAPIView):
    serializer_class = FavouriteRestaurantSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        if self.request.user.role == "super_admin":
            return FavouriteRestaurant.objects.all()
        return FavouriteRestaurant.objects.filter(customer=self.request.user).select_related("restaurant")

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class CustomerFavouriteDeleteView(generics.DestroyAPIView):
    serializer_class = FavouriteRestaurantSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        if self.request.user.role == "super_admin":
            return FavouriteRestaurant.objects.all()
        return FavouriteRestaurant.objects.filter(customer=self.request.user)
