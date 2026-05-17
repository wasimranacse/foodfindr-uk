from rest_framework import serializers

from .models import FavouriteRestaurant


class FavouriteRestaurantSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source="restaurant.name", read_only=True)
    restaurant_slug = serializers.CharField(source="restaurant.slug", read_only=True)

    class Meta:
        model = FavouriteRestaurant
        fields = ("id", "customer", "restaurant", "restaurant_name", "restaurant_slug", "created_at")
        read_only_fields = ("customer", "created_at")

    def validate_restaurant(self, restaurant):
        if not restaurant.is_approved:
            raise serializers.ValidationError("Restaurant is not available.")
        return restaurant
