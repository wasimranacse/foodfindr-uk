from django.db.models import Avg
from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "id",
            "customer",
            "restaurant",
            "rating",
            "food_quality_rating",
            "service_rating",
            "value_rating",
            "delivery_rating",
            "comment",
            "is_approved",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("customer", "restaurant", "is_approved", "created_at", "updated_at")


def refresh_restaurant_review_stats(restaurant):
    approved_reviews = restaurant.reviews.filter(is_approved=True)
    stats = approved_reviews.aggregate(average=Avg("rating"))
    restaurant.average_rating = stats["average"] or 0
    restaurant.review_count = approved_reviews.count()
    restaurant.save(update_fields=["average_rating", "review_count", "updated_at"])
