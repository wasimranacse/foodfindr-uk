from rest_framework import generics, permissions

from apps.restaurants.models import Restaurant
from apps.users.permissions import IsCustomer

from .models import Review
from .serializers import ReviewSerializer, refresh_restaurant_review_stats


class RestaurantReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsCustomer()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        return Review.objects.filter(
            restaurant_id=self.kwargs["restaurant_id"],
            restaurant__is_approved=True,
            is_approved=True,
        ).select_related("customer", "restaurant")

    def perform_create(self, serializer):
        restaurant = Restaurant.objects.get(pk=self.kwargs["restaurant_id"], is_approved=True)
        serializer.save(customer=self.request.user, restaurant=restaurant)


class CustomerReviewUpdateDeleteView(generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsCustomer]
    http_method_names = ["patch", "delete"]

    def get_queryset(self):
        if self.request.user.role == "super_admin":
            return Review.objects.all()
        return Review.objects.filter(customer=self.request.user)

    def perform_update(self, serializer):
        review = serializer.save()
        refresh_restaurant_review_stats(review.restaurant)

    def perform_destroy(self, instance):
        restaurant = instance.restaurant
        instance.delete()
        refresh_restaurant_review_stats(restaurant)
