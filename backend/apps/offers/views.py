from django.db.models import Q
from django.utils import timezone
from rest_framework import generics, permissions

from apps.users.permissions import IsRestaurantOwner

from .models import Offer
from .serializers import OfferSerializer


def active_offer_queryset():
    now = timezone.now()
    return Offer.objects.filter(
        is_active=True,
        restaurant__is_approved=True,
    ).filter(
        Q(start_date__isnull=True) | Q(start_date__lte=now),
        Q(end_date__isnull=True) | Q(end_date__gte=now),
    )


class ActiveOfferListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = OfferSerializer

    def get_queryset(self):
        return active_offer_queryset().select_related("restaurant")


class RestaurantOfferListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = OfferSerializer

    def get_queryset(self):
        return active_offer_queryset().filter(restaurant_id=self.kwargs["restaurant_id"])


class OwnerOfferCreateView(generics.CreateAPIView):
    serializer_class = OfferSerializer
    permission_classes = [IsRestaurantOwner]


class OwnerOfferUpdateDeleteView(generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = OfferSerializer
    permission_classes = [IsRestaurantOwner]
    http_method_names = ["patch", "delete"]

    def get_queryset(self):
        if self.request.user.role == "super_admin":
            return Offer.objects.all()
        return Offer.objects.filter(restaurant__owner=self.request.user)
