"""
Weather models for tracking location and weather data.

Stores user weather searches and associated weather metrics for
reporting and caching purposes.
"""
from django.db import models


class SearchHistory(models.Model):
    """Weather search record with associated weather data."""

    city_name = models.CharField(
        max_length=100, db_index=True, help_text="City name searched"
    )
    temperature = models.FloatField(
        null=True, blank=True, help_text="Current temperature in Celsius"
    )
    feels_like = models.FloatField(
        null=True, blank=True, help_text="Feels-like temperature"
    )
    humidity = models.IntegerField(
        null=True, blank=True, help_text="Humidity percentage"
    )
    wind_speed = models.FloatField(
        null=True, blank=True, help_text="Wind speed in km/h"
    )
    description = models.CharField(
        max_length=120, null=True, blank=True, help_text="Weather description"
    )
    icon = models.CharField(
        max_length=8, null=True, blank=True, help_text="Weather icon code"
    )
    searched_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-searched_at"]
        verbose_name_plural = "Search Histories"
        indexes = [
            models.Index(fields=["city_name", "-searched_at"]),
        ]

    def __str__(self):
        return f"{self.city_name} - {self.searched_at.strftime('%Y-%m-%d %H:%M')}"
