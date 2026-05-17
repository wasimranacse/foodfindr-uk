from django.db import models


class Offer(models.Model):
    class OfferType(models.TextChoices):
        PERCENTAGE = "percentage", "Percentage"
        FIXED_AMOUNT = "fixed_amount", "Fixed amount"
        FREE_ITEM = "free_item", "Free item"
        BUNDLE = "bundle", "Bundle"

    restaurant = models.ForeignKey(
        "restaurants.Restaurant",
        on_delete=models.CASCADE,
        related_name="offers",
    )
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    offer_type = models.CharField(
        max_length=32,
        choices=OfferType.choices,
        default=OfferType.PERCENTAGE,
    )
    discount_value = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    minimum_spend = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    terms = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["restaurant", "is_active"]),
            models.Index(fields=["start_date", "end_date"]),
            models.Index(fields=["is_featured", "is_active"]),
        ]

    def __str__(self) -> str:
        return self.title
