"""
Blog models for content management with categories, posts, and SEO-friendly URLs.

Supports organizing blog posts by category with automatic slug generation
and content previewing.
"""
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """Blog post category for organizing content."""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Post(models.Model):
    """Blog post with publication status and auto-generated slug."""

    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to="posts/", null=True, blank=True)

    slug = models.SlugField(unique=True, blank=True, db_index=True)
    is_published = models.BooleanField(default=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["is_published", "-created_at"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Auto-generate unique slug from title if not provided."""
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)

    def _generate_unique_slug(self):
        """Generate a unique slug, appending counter if needed."""
        base_slug = slugify(self.title)
        slug = base_slug
        counter = 1

        while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

    def short_description(self):
        """Return first 30 words of content as preview."""
        words = self.content.split()
        if len(words) > 30:
            return " ".join(words[:30]) + "..."
        return self.content
