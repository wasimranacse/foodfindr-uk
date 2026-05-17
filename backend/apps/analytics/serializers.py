from rest_framework import serializers

from .models import LocationSearchLog, RestaurantAnalyticsEvent


class RestaurantAnalyticsEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantAnalyticsEvent
        fields = ("id", "restaurant", "customer", "event_type", "metadata", "created_at")
        read_only_fields = ("customer", "created_at")

    def validate_event_type(self, event_type):
        valid_event_types = {
            choice.value for choice in RestaurantAnalyticsEvent.EventType
        }
        if event_type not in valid_event_types:
            raise serializers.ValidationError("Unsupported analytics event type.")
        return event_type

    def validate_restaurant(self, restaurant):
        if restaurant and not restaurant.is_approved:
            raise serializers.ValidationError("Restaurant is not available.")
        return restaurant


class RestaurantAnalyticsSummarySerializer(serializers.Serializer):
    restaurant = serializers.IntegerField()
    events = serializers.DictField(child=serializers.IntegerField())
    total_events = serializers.IntegerField()


class LocationSearchLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationSearchLog
        fields = ("id", "customer", "query", "postcode", "latitude", "longitude", "created_at")
        read_only_fields = ("customer", "created_at")
