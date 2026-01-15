"""Django admin configuration for weather data.

Customizes the admin interface for managing weather search history.
"""
from django.contrib import admin
from .models import SearchHistory


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    """Admin interface for weather search records."""

    list_display = [
        "city_name",
        "temperature",
        "humidity",
        "description",
        "searched_at",
    ]
    list_filter = ["city_name", "searched_at"]
    search_fields = ["city_name"]
    readonly_fields = ["searched_at"]
    ordering = ["-searched_at"]
    date_hierarchy = "searched_at"
    
    # Allow editing all fields except searched_at
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return ["searched_at"]
        return []