from rest_framework import serializers

from .models import Offer


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = (
            "id",
            "restaurant",
            "title",
            "description",
            "offer_type",
            "discount_value",
            "minimum_spend",
            "start_date",
            "end_date",
            "terms",
            "is_active",
            "is_featured",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")

    def validate_restaurant(self, restaurant):
        request = self.context["request"]
        if request.user.role != "super_admin" and restaurant.owner_id != request.user.id:
            raise serializers.ValidationError("You can only manage offers for your own restaurant.")
        return restaurant
