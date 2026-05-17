from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Restaurant(models.Model):
    class SubscriptionPlan(models.TextChoices):
        FREE = "free", "Free"
        PREMIUM = "premium", "Premium"
        PRO = "pro", "Pro"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="restaurants",
    )
    name = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    country = models.ForeignKey(
        "locations.Country",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="restaurants",
    )
    city = models.ForeignKey(
        "locations.City",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="restaurants",
    )
    area = models.ForeignKey(
        "locations.Area",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="restaurants",
    )
    address = models.CharField(max_length=255, blank=True)
    postcode = models.CharField(max_length=20, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    cuisine_types = models.ManyToManyField(
        "locations.Cuisine",
        blank=True,
        related_name="restaurants",
    )
    price_level = models.PositiveSmallIntegerField(
        default=2,
        validators=[MinValueValidator(1), MaxValueValidator(4)],
    )
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )
    review_count = models.PositiveIntegerField(default=0)
    trust_score = models.PositiveSmallIntegerField(default=0)
    food_hygiene_rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )
    food_hygiene_rating_date = models.DateField(null=True, blank=True)
    food_hygiene_source = models.CharField(max_length=120, blank=True)
    local_authority_name = models.CharField(max_length=160, blank=True)
    fsa_business_id = models.CharField(max_length=80, blank=True)
    google_place_id = models.CharField(max_length=160, blank=True)
    google_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )
    google_review_count = models.PositiveIntegerField(default=0)
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    minimum_order = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    average_preparation_time_minutes = models.PositiveSmallIntegerField(default=30)
    service_radius_km = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_open = models.BooleanField(default=False)
    is_busy = models.BooleanField(default=False)
    delivery_available = models.BooleanField(default=False)
    collection_available = models.BooleanField(default=False)
    dine_in_available = models.BooleanField(default=False)
    phone_order_available = models.BooleanField(default=False)
    halal_available = models.BooleanField(default=False)
    vegan_available = models.BooleanField(default=False)
    vegetarian_available = models.BooleanField(default=False)
    gluten_free_available = models.BooleanField(default=False)
    direct_order_url = models.URLField(blank=True)
    uber_eats_url = models.URLField(blank=True)
    deliveroo_url = models.URLField(blank=True)
    just_eat_url = models.URLField(blank=True)
    is_verified = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    featured_until = models.DateTimeField(null=True, blank=True)
    sponsored_rank_boost = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    subscription_plan = models.CharField(
        max_length=32,
        choices=SubscriptionPlan.choices,
        default=SubscriptionPlan.FREE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["is_approved", "is_open"]),
            models.Index(fields=["city", "area"]),
            models.Index(fields=["name"]),
            models.Index(fields=["postcode"]),
            models.Index(fields=["is_featured", "is_premium"]),
        ]

    def __str__(self) -> str:
        return self.name


class RestaurantOpeningHour(models.Model):
    class DayOfWeek(models.IntegerChoices):
        MONDAY = 0, "Monday"
        TUESDAY = 1, "Tuesday"
        WEDNESDAY = 2, "Wednesday"
        THURSDAY = 3, "Thursday"
        FRIDAY = 4, "Friday"
        SATURDAY = 5, "Saturday"
        SUNDAY = 6, "Sunday"

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="opening_hours",
    )
    day_of_week = models.PositiveSmallIntegerField(choices=DayOfWeek.choices)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ["day_of_week", "opening_time"]
        constraints = [
            models.UniqueConstraint(
                fields=["restaurant", "day_of_week"],
                name="unique_opening_hours_per_restaurant_day",
            )
        ]

    def __str__(self) -> str:
        return f"{self.restaurant} {self.get_day_of_week_display()}"
