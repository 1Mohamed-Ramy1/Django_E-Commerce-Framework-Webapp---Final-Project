"""Django admin configuration for blog models.

Customizes the admin interface for managing blog posts and categories.
"""
from django.contrib import admin
from .models import Post, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for blog categories."""

    list_display = ["name"]
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin interface for blog posts with publication control."""

    list_display = ["title", "is_published", "created_at"]
    list_filter = ["is_published", "created_at"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ["slug", "created_at", "updated_at"]
    ordering = ["-created_at"]

    fieldsets = (
        ("Content", {"fields": ("title", "content")}),
        ("Media", {"fields": ("image",)}),
        ("Publishing", {"fields": ("is_published", "slug")}),
        ("Metadata", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )
