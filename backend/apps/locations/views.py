from rest_framework import generics, permissions

from apps.restaurants.utils import calculate_distance_km

from .models import Area, City, Country
from .serializers import AreaSerializer, CitySerializer, CountrySerializer


class CountryListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CountrySerializer
    queryset = Country.objects.all().order_by("name")


class CityListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CitySerializer

    def get_queryset(self):
        queryset = City.objects.select_related("country").order_by("name")
        if country := self.request.query_params.get("country"):
            queryset = queryset.filter(country__code__iexact=country)
        return queryset


class AreaListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = AreaSerializer

    def get_queryset(self):
        queryset = Area.objects.select_related("city", "city__country").order_by("name")
        if city := self.request.query_params.get("city"):
            queryset = queryset.filter(city__slug=city)
        return queryset


class PostcodeLookupView(AreaListView):
    def get_queryset(self):
        postcode = self.request.query_params.get("postcode", "").strip().upper()
        prefix = postcode.split(" ")[0] if postcode else ""
        return (
            Area.objects.select_related("city", "city__country")
            .filter(postcode_prefix__istartswith=prefix[:4])
            .order_by("name")
        )


class NearbyAreasView(AreaListView):
    def list(self, request, *args, **kwargs):
        lat = request.query_params.get("lat")
        lng = request.query_params.get("lng")
        areas = list(self.get_queryset())
        for area in areas:
            area.distance_km = calculate_distance_km(lat, lng, area.latitude, area.longitude)
        areas.sort(key=lambda area: area.distance_km if area.distance_km is not None else float("inf"))
        page = self.paginate_queryset(areas)
        if page is not None:
            return self.get_paginated_response(self.get_serializer(page, many=True).data)
        return super().list(request, *args, **kwargs)
