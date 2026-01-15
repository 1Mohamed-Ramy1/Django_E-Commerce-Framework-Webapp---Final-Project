"""
Event and promotion models for managing sales, discounts, and special offers.

Supports event scheduling, status tracking, discount management, and
countdown timers for time-sensitive promotions.
"""
import uuid
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class EventManager(models.Manager):
    """Custom manager for filtering events by status."""

    def running(self):
        """Get events that have started but not ended."""
        return self.filter(event_date__gte=timezone.now())

    def active(self):
        """Get currently active, non-ended events."""
        return self.filter(is_active=True, event_date__gte=timezone.now()).order_by(
            "event_date"
        )


class Event(models.Model):
    """Promotional event with scheduling, discounts, and status tracking."""

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("live", "Live"),
        ("soon", "Soon"),
        ("end", "End"),
        ("cancelled", "Cancelled"),
    ]
    EVENT_TYPE_CHOICES = [
        ("sale", "Sale"),
        ("discount", "Discount"),
        ("offer", "Special Offer"),
        ("launch", "Product Launch"),
        ("flash", "Flash Sale"),
        ("seasonal", "Seasonal"),
    ]

    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    event_type = models.CharField(
        max_length=20, choices=EVENT_TYPE_CHOICES, default="sale"
    )

    event_date = models.DateTimeField(db_index=True)
    end_date = models.DateTimeField(null=True, blank=True)

    discount_percentage = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Discount percentage (0-100)",
    )
    
    # Categories this event applies to (ManyToMany for multiple category discounts)
    categories = models.ManyToManyField(
        'shop.Category',
        related_name='events',
        blank=True,
        help_text="Categories that will have this discount applied"
    )

    banner_image = models.ImageField(upload_to="events/", blank=True, null=True)
    is_active = models.BooleanField(default=True, db_index=True)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default="pending", db_index=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    objects = EventManager()

    class Meta:
        ordering = ["event_date"]
        indexes = [
            models.Index(fields=["is_active", "event_date"]),
            models.Index(fields=["status", "event_date"]),
        ]

    def __str__(self):
        return f"{self.name} - {self.get_event_type_display()}"

    def countdown(self):
        """Calculate time remaining until event starts, or None if already passed."""
        delta = self.event_date - timezone.now()
        return delta if delta.total_seconds() > 0 else None

    @property
    def countdown_hours(self):
        """Get hours remaining until event starts."""
        delta = self.countdown()
        if delta:
            return delta.seconds // 3600
        return 0

    @property
    def is_ongoing(self):
        """Check if event is currently in progress."""
        now = timezone.now()
        if self.end_date:
            return self.event_date <= now <= self.end_date
        return self.event_date <= now

    @property
    def is_upcoming(self):
        """Check if event has not yet started."""
        return self.event_date > timezone.now()

    @property
    def is_ended(self):
        """Check if event has completed."""
        now = timezone.now()
        if self.end_date:
            return now > self.end_date
        return False

    @property
    def is_cancelled(self):
        """Check if event was cancelled."""
        return self.status == "cancelled"
    
    def apply_discount_to_categories(self):
        """
        Apply this event's discount to all products in selected categories.
        Returns list of updated products.
        """
        if not self.is_active or self.discount_percentage == 0:
            return []
        
        from shop.models import Product
        updated_products = []
        
        for category in self.categories.all():
            products = Product.objects.filter(category_ref=category)
            for product in products:
                # Store original price if not already stored
                if not hasattr(product, '_original_price'):
                    product._original_price = product.price
                updated_products.append(product)
        
        return updated_products
    
    def get_discounted_price(self, original_price):
        """Calculate discounted price based on event's discount percentage."""
        if not self.is_active or self.discount_percentage == 0:
            return original_price
        
        discount_amount = original_price * (self.discount_percentage / 100)
        return original_price - discount_amount
    
    def has_category_discount(self, category):
        """Check if this event applies discount to given category."""
        if not self.is_active:
            return False
        return self.categories.filter(id=category.id).exists()
