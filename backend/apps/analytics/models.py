from django.conf import settings
from django.db import models


class RestaurantAnalyticsEvent(models.Model):
    class EventType(models.TextChoices):
        PROFILE_VIEW = "profile_view", "Profile view"
        MENU_VIEW = "menu_view", "Menu view"
        OFFER_CLAIM_CLICK = "offer_claim_click", "Offer claim click"
        CALL_CLICK = "call_click", "Call click"
        DIRECTION_CLICK = "direction_click", "Direction click"
        FAVOURITE_SAVE = "favourite_save", "Favourite save"
        ORDER_UBER_EATS_CLICK = "order_uber_eats_click", "Order Uber Eats click"
        ORDER_DELIVEROO_CLICK = "order_deliveroo_click", "Order Deliveroo click"
        ORDER_JUST_EAT_CLICK = "order_just_eat_click", "Order Just Eat click"
        ORDER_DIRECT_CLICK = "order_direct_click", "Order direct click"

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
