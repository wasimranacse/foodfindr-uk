from django.conf import settings
from django.db import models


class Favourite(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favourites",
    )
    restaurant = models.ForeignKey(
        "restaurants.Restaurant",
        on_delete=models.CASCADE,
        related_name="favourited_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["customer", "restaurant"],
                name="unique_favourite_per_customer_restaurant",
            )
        ]
        indexes = [models.Index(fields=["customer", "created_at"])]

    def __str__(self) -> str:
        return f"{self.customer} favourite {self.restaurant}"
