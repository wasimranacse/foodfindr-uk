from django.urls import path

from .views import AreaListView, CityListView, CountryListView, NearbyAreasView, PostcodeLookupView

urlpatterns = [
    path("locations/countries/", CountryListView.as_view(), name="location-country-list"),
    path("locations/cities/", CityListView.as_view(), name="location-city-list"),
    path("locations/areas/", AreaListView.as_view(), name="location-area-list"),
    path("locations/postcode-lookup/", PostcodeLookupView.as_view(), name="location-postcode-lookup"),
    path("locations/nearby-areas/", NearbyAreasView.as_view(), name="location-nearby-areas"),
]
