from django.conf import settings
from django.db import models


class RestaurantAnalyticsEvent(models.Model):
    class EventType(models.TextChoices):
        VIEW_MENU = "view_menu", "View menu"
        CALL_RESTAURANT = "call_restaurant", "Call restaurant"
        GET_DIRECTIONS = "get_directions", "Get directions"
        CLAIM_OFFER = "claim_offer", "Claim offer"
        ORDER_UBER_EATS = "order_uber_eats", "Order on Uber Eats"
        ORDER_DELIVEROO = "order_deliveroo", "Order on Deliveroo"
        ORDER_JUST_EAT = "order_just_eat", "Order on Just Eat"
        ORDER_DIRECTLY = "order_directly", "Order directly"

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="restaurant_analytics_events",
    )
    restaurant = models.ForeignKey(
        "restaurants.Restaurant",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="analytics_events",
    )
    event_type = models.CharField(max_length=64, choices=EventType.choices)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["event_type", "created_at"]),
            models.Index(fields=["restaurant", "created_at"]),
            models.Index(fields=["customer", "created_at"]),
        ]


class LocationSearchLog(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="location_search_logs",
    )
    query = models.CharField(max_length=255, blank=True)
    postcode = models.CharField(max_length=20, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["postcode", "created_at"]),
            models.Index(fields=["customer", "created_at"]),
        ]


AnalyticsEvent = RestaurantAnalyticsEvent
