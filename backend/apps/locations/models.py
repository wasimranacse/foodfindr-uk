from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=120, unique=True)
    code = models.CharField(max_length=2, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "countries"

    def __str__(self) -> str:
        return self.name


class City(models.Model):
    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        related_name="cities",
    )
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["country", "slug"],
                name="unique_city_slug_per_country",
            )
        ]
        verbose_name_plural = "cities"

    def __str__(self) -> str:
        return f"{self.name}, {self.country.code}"


class Area(models.Model):
    city = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        related_name="areas",
    )
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140)
    postcode_prefix = models.CharField(max_length=12, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["city", "slug"],
                name="unique_area_slug_per_city",
            )
        ]
        indexes = [models.Index(fields=["postcode_prefix"])]

    def __str__(self) -> str:
        return f"{self.name}, {self.city.name}"


class Cuisine(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    icon = models.CharField(max_length=80, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Location(models.Model):
    country = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    area = models.CharField(max_length=120, blank=True)
    borough_or_district = models.CharField(max_length=120, blank=True)
    postcode = models.CharField(max_length=20, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["country", "city"]),
            models.Index(fields=["postcode"]),
        ]

    def __str__(self) -> str:
        return ", ".join(part for part in [self.area, self.city, self.country] if part)
