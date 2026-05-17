from django.db import models


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
