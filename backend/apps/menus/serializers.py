from rest_framework import serializers

from apps.restaurants.models import Restaurant

from .models import MenuCategory, MenuItem


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = (
            "id",
            "restaurant",
            "category",
            "name",
            "description",
            "price",
            "image_url",
            "is_available",
            "is_halal",
            "is_vegan",
            "is_vegetarian",
            "is_gluten_free",
            "allergens",
            "calories",
            "spicy_level",
            "preparation_time_minutes",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")

    def validate_restaurant(self, restaurant):
        request = self.context["request"]
        if request.user.role != "super_admin" and restaurant.owner_id != request.user.id:
            raise serializers.ValidationError("You can only manage your own restaurant menu.")
        return restaurant

    def validate(self, attrs):
        restaurant = attrs.get("restaurant") or getattr(self.instance, "restaurant", None)
        category = attrs.get("category") or getattr(self.instance, "category", None)
        if restaurant and category and category.restaurant_id != restaurant.id:
            raise serializers.ValidationError("Menu item category must belong to the restaurant.")
        return attrs


class MenuCategorySerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = MenuCategory
        fields = (
            "id",
            "restaurant",
            "name",
            "description",
            "display_order",
            "is_active",
            "items",
        )

    def validate_restaurant(self, restaurant):
        request = self.context["request"]
        if request.user.role != "super_admin" and restaurant.owner_id != request.user.id:
            raise serializers.ValidationError("You can only manage your own restaurant menu.")
        return restaurant
