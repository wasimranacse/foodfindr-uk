from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response

from apps.restaurants.models import Restaurant
from apps.users.permissions import IsRestaurantOwner

from .models import RestaurantAnalyticsEvent
from .serializers import RestaurantAnalyticsEventSerializer


class AnalyticsEventCreateView(generics.CreateAPIView):
    serializer_class = RestaurantAnalyticsEventSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = self.request.user
        customer = user if user.is_authenticated and user.is_email_verified else None
        serializer.save(customer=customer)


class OwnerRestaurantAnalyticsView(generics.GenericAPIView):
    permission_classes = [IsRestaurantOwner]

    def get(self, request, restaurant_id):
        if request.user.role == "super_admin":
            restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
        else:
            restaurant = get_object_or_404(Restaurant, pk=restaurant_id, owner=request.user)
        event_counts = dict(
            RestaurantAnalyticsEvent.objects.filter(restaurant=restaurant)
            .values_list("event_type")
            .annotate(count=Count("id"))
        )
        return Response(
            {
                "restaurant": restaurant.id,
                "events": event_counts,
                "total_events": sum(event_counts.values()),
            }
        )
