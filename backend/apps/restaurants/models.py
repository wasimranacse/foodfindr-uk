from django.conf import settings
from django.db import models


class Restaurant(models.Model):
    class ApprovalStatus(models.TextChoices):
        DRAFT = "draft", "Draft"
        PENDING = "pending", "Pending approval"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="restaurants",
    )
    location = models.ForeignKey(
        "locations.Location",
        on_delete=models.PROTECT,
        related_name="restaurants",
    )
    name = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    phone_number = models.CharField(max_length=40, blank=True)
    website_url = models.URLField(blank=True)
    direct_order_url = models.URLField(blank=True)
    uber_eats_url = models.URLField(blank=True)
    deliveroo_url = models.URLField(blank=True)
    just_eat_url = models.URLField(blank=True)
    is_phone_order_available = models.BooleanField(default=False)
    is_collection_available = models.BooleanField(default=False)
    is_delivery_available = models.BooleanField(default=False)
    approval_status = models.CharField(
        max_length=32,
        choices=ApprovalStatus.choices,
        default=ApprovalStatus.DRAFT,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["approval_status", "created_at"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self) -> str:
        return self.name
