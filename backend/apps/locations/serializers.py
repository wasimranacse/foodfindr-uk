from rest_framework import serializers

from .models import Area, City, Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("id", "name", "code")


class CitySerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source="country.name", read_only=True)

    class Meta:
        model = City
        fields = ("id", "country", "country_name", "name", "slug")


class AreaSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source="city.name", read_only=True)
    distance_km = serializers.FloatField(read_only=True)

    class Meta:
        model = Area
        fields = (
            "id",
            "city",
            "city_name",
            "name",
            "slug",
            "postcode_prefix",
            "latitude",
            "longitude",
            "distance_km",
        )
