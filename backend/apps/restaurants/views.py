from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.permissions import IsAdminRole, IsRestaurantOwner

from .models import Restaurant
from .serializers import RestaurantApprovalSerializer, RestaurantSerializer
from .utils import (
    calculate_distance_km,
    calculate_trust_score,
    estimate_delivery_time_minutes,
    restaurant_has_active_offer,
    smart_rank_restaurants,
)


class RestaurantQueryMixin:
    serializer_class = RestaurantSerializer
    default_sort = "-trust_score"

    def get_base_queryset(self):
        return (
            Restaurant.objects.filter(is_approved=True)
            .select_related("country", "city", "area", "owner")
            .prefetch_related("cuisine_types", "opening_hours", "offers")
        )

    def filter_queryset_from_params(self, queryset):
        params = self.request.query_params
        if city := params.get("city"):
            queryset = queryset.filter(Q(city__slug=city) | Q(city__name__iexact=city))
        if area := params.get("area"):
            queryset = queryset.filter(Q(area__slug=area) | Q(area__name__iexact=area))
        if cuisine := params.get("cuisine"):
            queryset = queryset.filter(
                Q(cuisine_types__slug=cuisine) | Q(cuisine_types__name__iexact=cuisine)
            )
        if price_level := params.get("price_level"):
            queryset = queryset.filter(price_level=price_level)
        if rating := params.get("rating"):
            queryset = queryset.filter(average_rating__gte=rating)
        if hygiene_rating := params.get("hygiene_rating"):
            queryset = queryset.filter(food_hygiene_rating__gte=hygiene_rating)
        boolean_filters = {
            "halal": "halal_available",
            "vegan": "vegan_available",
            "vegetarian": "vegetarian_available",
            "gluten_free": "gluten_free_available",
            "delivery_available": "delivery_available",
            "collection_available": "collection_available",
            "open_now": "is_open",
        }
        for param_name, field_name in boolean_filters.items():
            if params.get(param_name) in {"1", "true", "True"}:
                queryset = queryset.filter(**{field_name: True})
        if params.get("active_offers") in {"1", "true", "True"}:
            now = timezone.now()
            queryset = queryset.filter(
                offers__is_active=True,
            ).filter(
                Q(offers__start_date__isnull=True) | Q(offers__start_date__lte=now),
                Q(offers__end_date__isnull=True) | Q(offers__end_date__gte=now),
            )
        return queryset.distinct()

    def sort_and_annotate(self, queryset):
        params = self.request.query_params
        ordering = params.get("sort", self.default_sort)
        lat = params.get("lat")
        lng = params.get("lng")

        restaurants = list(queryset)
        for restaurant in restaurants:
            restaurant.distance_km = calculate_distance_km(
                lat,
                lng,
                restaurant.latitude,
                restaurant.longitude,
            )
            restaurant.estimated_delivery_time_minutes = estimate_delivery_time_minutes(
                restaurant,
                lat,
                lng,
            )
            restaurant.smart_rank_score = None

        radius = params.get("radius")
        if radius and lat and lng:
            try:
                radius_km = float(radius)
            except ValueError:
                radius_km = None
            if radius_km is not None:
                restaurants = [
                    restaurant
                    for restaurant in restaurants
                    if restaurant.distance_km is not None
                    and restaurant.distance_km <= radius_km
                ]

        if ordering in {"distance", "delivery_time", "offers", "smart"}:
            if ordering == "distance":
                restaurants.sort(
                    key=lambda item: item.distance_km
                    if item.distance_km is not None
                    else float("inf")
                )
            elif ordering == "delivery_time":
                restaurants.sort(key=lambda item: item.estimated_delivery_time_minutes)
            elif ordering == "offers":
                restaurants.sort(key=lambda item: restaurant_has_active_offer(item), reverse=True)
            else:
                ranked = smart_rank_restaurants(restaurants, lat, lng)
                for ranked_item in ranked:
                    ranked_item.restaurant.smart_rank_score = ranked_item.score
                    ranked_item.restaurant.distance_km = ranked_item.distance_km
                    ranked_item.restaurant.estimated_delivery_time_minutes = (
                        ranked_item.estimated_delivery_time_minutes
                    )
                restaurants = [ranked_item.restaurant for ranked_item in ranked]
            return restaurants

        ordering_map = {
            "rating": "-average_rating",
            "-rating": "-average_rating",
            "review_count": "-review_count",
            "-review_count": "-review_count",
            "trust_score": "-trust_score",
            "-trust_score": "-trust_score",
            "price": "price_level",
            "-price": "-price_level",
        }
        return queryset.order_by(ordering_map.get(ordering, "-trust_score"), "name")

    def list_response(self, queryset):
        result = self.sort_and_annotate(queryset)
        page = self.paginate_queryset(result)
        if page is not None:
            return self.get_paginated_response(self.get_serializer(page, many=True).data)
        return Response(self.get_serializer(result, many=True).data)


class RestaurantListView(RestaurantQueryMixin, generics.ListAPIView):
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return self.filter_queryset_from_params(self.get_base_queryset())

    def list(self, request, *args, **kwargs):
        return self.list_response(self.get_queryset())


class NearbyRestaurantView(RestaurantListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params
        postcode = params.get("postcode")
        if postcode:
            queryset = queryset.filter(postcode__istartswith=postcode.strip()[:4])
        radius = params.get("radius")
        lat = params.get("lat")
        lng = params.get("lng")
        if radius and lat and lng:
            return list(queryset)
        return queryset


class TopRatedRestaurantView(RestaurantListView):
    default_sort = "rating"

    def get_queryset(self):
        return super().get_queryset().filter(review_count__gt=0)


class FeaturedRestaurantView(RestaurantListView):
    def get_queryset(self):
        return super().get_queryset().filter(is_featured=True)


class RestaurantOffersView(RestaurantListView):
    default_sort = "offers"

    def get_queryset(self):
        now = timezone.now()
        return super().get_queryset().filter(
            offers__is_active=True,
        ).filter(
            Q(offers__start_date__isnull=True) | Q(offers__start_date__lte=now),
            Q(offers__end_date__isnull=True) | Q(offers__end_date__gte=now),
        )


class RestaurantDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RestaurantSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Restaurant.objects.filter(is_approved=True).select_related(
            "country", "city", "area", "owner"
        ).prefetch_related("cuisine_types", "opening_hours")


class OwnerRestaurantCreateView(generics.CreateAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [IsRestaurantOwner]


class OwnerRestaurantUpdateView(generics.UpdateAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [IsRestaurantOwner]
    http_method_names = ["patch"]

    def get_queryset(self):
        if self.request.user.role == "super_admin":
            return Restaurant.objects.all()
        return Restaurant.objects.filter(owner=self.request.user)


class AdminRestaurantApprovalView(APIView):
    permission_classes = [IsAdminRole]

    def post(self, request, pk, action):
        serializer = RestaurantApprovalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        restaurant = get_object_or_404(Restaurant, pk=pk)
        restaurant.is_approved = action == "approve"
        if action == "approve":
            restaurant.trust_score = calculate_trust_score(restaurant)
        restaurant.save(update_fields=["is_approved", "trust_score", "updated_at"])
        return Response(RestaurantSerializer(restaurant).data, status=status.HTTP_200_OK)
