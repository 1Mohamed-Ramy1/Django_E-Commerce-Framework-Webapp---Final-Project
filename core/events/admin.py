"""Django admin configuration for events.

Customizes the admin interface for managing promotional events and sales.
"""
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Admin interface for promotional events with status tracking."""

    list_display = [
        "name",
        "event_type",
        "discount_percentage",
        "event_date",
        "is_active",
        "is_ongoing",
        "created_at",
    ]
    list_filter = ["event_type", "status", "is_active", "created_at"]
    search_fields = ["name", "description"]
    list_editable = ["is_active"]
    readonly_fields = ["uid", "created_at", "is_ongoing_display"]
    date_hierarchy = "event_date"
    ordering = ["-event_date"]

    fieldsets = (
        ("Basic Information", {"fields": ("name", "description", "event_type", "is_active")}),
        ("Dates", {"fields": ("event_date", "end_date")}),
        ("Discount", {"fields": ("discount_percentage",)}),
        ("Media", {"fields": ("banner_image",)}),
        (
            "System",
            {"fields": ("uid", "status", "created_at", "is_ongoing_display"), "classes": ("collapse",)},
        ),
    )
    
    def is_ongoing(self, obj):
        """Display ongoing status as emoji."""
        return '🟢 Yes' if obj.is_ongoing else '🔴 No'
    is_ongoing.short_description = 'Active Now'
    
    def is_ongoing_display(self, obj):
        """Display ongoing status in readonly field."""
        return '🟢 Yes' if obj.is_ongoing else '🔴 No'
    is_ongoing_display.short_description = 'Active Now'
