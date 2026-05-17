from django.utils.text import slugify
from rest_framework import serializers

from apps.locations.models import Area, City, Country, Cuisine

from .models import Restaurant, RestaurantOpeningHour


class CuisineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuisine
        fields = ("id", "name", "slug", "icon")


class RestaurantOpeningHourSerializer(serializers.ModelSerializer):
    day_name = serializers.CharField(source="get_day_of_week_display", read_only=True)

    class Meta:
        model = RestaurantOpeningHour
        fields = (
            "id",
            "day_of_week",
            "day_name",
            "opening_time",
            "closing_time",
            "is_closed",
        )


class RestaurantSerializer(serializers.ModelSerializer):
    cuisine_types = CuisineSerializer(many=True, read_only=True)
    cuisine_type_ids = serializers.PrimaryKeyRelatedField(
        queryset=Cuisine.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source="cuisine_types",
    )
    country_name = serializers.CharField(source="country.name", read_only=True)
    city_name = serializers.CharField(source="city.name", read_only=True)
    area_name = serializers.CharField(source="area.name", read_only=True)
    opening_hours = RestaurantOpeningHourSerializer(many=True, read_only=True)
    distance_km = serializers.FloatField(read_only=True)
    estimated_delivery_time_minutes = serializers.IntegerField(read_only=True)
    smart_rank_score = serializers.FloatField(read_only=True)

    class Meta:
        model = Restaurant
        fields = (
            "id",
            "owner",
            "name",
            "slug",
            "description",
            "country",
            "country_name",
            "city",
            "city_name",
            "area",
            "area_name",
            "address",
            "postcode",
            "latitude",
            "longitude",
            "phone",
            "website",
            "email",
            "cuisine_types",
            "cuisine_type_ids",
            "price_level",
            "average_rating",
            "review_count",
            "trust_score",
            "food_hygiene_rating",
            "food_hygiene_rating_date",
            "food_hygiene_source",
            "local_authority_name",
            "fsa_business_id",
            "google_place_id",
            "google_rating",
            "google_review_count",
            "delivery_fee",
            "minimum_order",
            "average_preparation_time_minutes",
            "service_radius_km",
            "is_open",
            "is_busy",
            "delivery_available",
            "collection_available",
            "dine_in_available",
            "phone_order_available",
            "halal_available",
            "vegan_available",
            "vegetarian_available",
            "gluten_free_available",
            "uber_eats_url",
            "deliveroo_url",
            "just_eat_url",
            "direct_order_url",
            "is_verified",
            "is_approved",
            "is_featured",
            "is_premium",
            "featured_until",
            "sponsored_rank_boost",
            "subscription_plan",
            "opening_hours",
            "distance_km",
            "estimated_delivery_time_minutes",
            "smart_rank_score",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "owner",
            "slug",
            "average_rating",
            "review_count",
            "trust_score",
            "is_verified",
            "is_approved",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        cuisines = validated_data.pop("cuisine_types", [])
        validated_data["owner"] = self.context["request"].user
        validated_data["slug"] = self._build_unique_slug(validated_data["name"])
        restaurant = super().create(validated_data)
        restaurant.cuisine_types.set(cuisines)
        return restaurant

    def update(self, instance, validated_data):
        cuisines = validated_data.pop("cuisine_types", None)
        restaurant = super().update(instance, validated_data)
        if cuisines is not None:
            restaurant.cuisine_types.set(cuisines)
        return restaurant

    def _build_unique_slug(self, name):
        base_slug = slugify(name)[:180] or "restaurant"
        slug = base_slug
        counter = 2
        while Restaurant.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug


class RestaurantApprovalSerializer(serializers.Serializer):
    reason = serializers.CharField(required=False, allow_blank=True)
