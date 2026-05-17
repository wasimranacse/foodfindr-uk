from django.db import models


class Menu(models.Model):
    restaurant = models.ForeignKey(
        "restaurants.Restaurant",
        on_delete=models.CASCADE,
        related_name="menus",
    )
    name = models.CharField(max_length=120, default="Main menu")
    menu_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["restaurant", "is_active"])]

    def __str__(self) -> str:
        return f"{self.restaurant} - {self.name}"
