"""Django admin configuration for user accounts.

Customizes the admin interface for user profiles, balance tracking,
password reset management, and role-based user management.
"""
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import PasswordReset, Profile, BalanceTransaction
from .permissions import is_admin_user, is_manager_user, get_user_tier


class CustomUserAdmin(BaseUserAdmin):
    """Enhanced User admin with role-based access control and three-tier hierarchy."""
    
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    
    list_display = ("username", "email", "first_name", "last_name", "get_tier", "is_staff", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups", "date_joined")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("-date_joined",)
    filter_horizontal = ("groups", "user_permissions")
    
    def get_tier(self, obj):
        """Display user tier."""
        tier = get_user_tier(obj)
        if tier == 'admin':
            return "👑 ADMIN"
        elif tier == 'manager':
            return "⭐ MANAGER"
        else:
            return "👤 USER"
    get_tier.short_description = "User Tier"
    
    def get_readonly_fields(self, request, obj=None):
        """Make admin user uneditable for non-admin users."""
        readonly = list(super().get_readonly_fields(request, obj))
        
        # If editing an admin user (ELOSTORA) - make everything readonly
        if obj and is_admin_user(obj):
            if not is_admin_user(request.user):
                # Non-admin users cannot edit any field
                return ["username", "password", "first_name", "last_name", "email", 
                        "is_active", "is_staff", "is_superuser", "groups", "user_permissions",
                        "last_login", "date_joined"]
            elif obj.username.lower() in ['admin', 'elostora']:
                # Even admin users cannot edit ELOSTORA admin account
                return ["username", "password", "first_name", "last_name", "email", 
                        "is_active", "is_staff", "is_superuser", "groups", "user_permissions",
                        "last_login", "date_joined"]
        
        return readonly
    
    def get_queryset(self, request):
        """Filter visible users based on current user's tier."""
        qs = super().get_queryset(request)
        
        if is_admin_user(request.user):
            # Admin can see all users
            return qs
        elif is_manager_user(request.user):
            # Manager can see only regular users and other managers (not admins/superusers)
            return qs.filter(is_superuser=False).exclude(username__in=['admin', 'ELOSTORA'])
        else:
            # Regular users can't access this
            return qs.none()
    
    def has_delete_permission(self, request, obj=None):
        """Control delete permissions - ADMIN users cannot be deleted."""
        if obj:
            # Cannot delete ADMIN tier users (ELOSTORA, admin, superusers)
            if is_admin_user(obj):
                return False
            # Manager can delete regular users only
            if is_manager_user(request.user):
                return not is_manager_user(obj)  # Cannot delete other managers
        return is_admin_user(request.user)
    
    def has_add_permission(self, request):
        """Only admin and managers can add users."""
        return is_admin_user(request.user) or is_manager_user(request.user)
    
    def has_change_permission(self, request, obj=None):
        """Control change permissions based on user tier."""
        if not super().has_change_permission(request, obj):
            return False
        
        if obj is None:
            # List view - allow if admin or manager
            return is_admin_user(request.user) or is_manager_user(request.user)
        
        # Cannot edit ADMIN tier users (ELOSTORA, admin)
        if is_admin_user(obj):
            return False
        
        # Manager can edit regular users and other managers
        if is_manager_user(request.user):
            return True
        
        # Admin can edit anyone except ADMIN tier
        return is_admin_user(request.user)
    
    def has_view_permission(self, request, obj=None):
        """Control view permissions based on user tier."""
        if obj is None:
            return is_admin_user(request.user) or is_manager_user(request.user)
        
        if is_admin_user(obj):
            return is_admin_user(request.user)
        
        return is_admin_user(request.user) or is_manager_user(request.user)


# Unregister default User admin and register custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin interface for user profiles."""

    list_display = ["user", "phone", "balance", "loyalty_points", "blocked"]
    list_filter = ["blocked", "warning"]
    search_fields = ["user__username", "user__email", "phone"]
    ordering = ["user__username"]

    fieldsets = (
        ("User", {"fields": ("user",)}),
        ("Contact", {"fields": ("phone", "address", "image")}),
        ("Account Status", {"fields": ("warning", "blocked")}),
        (
            "Balance & Loyalty",
            {"fields": ("balance", "total_spent", "last_purchase", "loyalty_points", "points")},
        ),
    )


@admin.register(BalanceTransaction)
class BalanceTransactionAdmin(admin.ModelAdmin):
    """Admin interface for wallet transactions."""

    list_display = ["user", "type", "amount", "reference", "created_at"]
    list_filter = ["type", "created_at"]
    search_fields = ["user__username", "reference"]
    readonly_fields = ["created_at"]
    ordering = ["-created_at"]


@admin.register(PasswordReset)
class PasswordResetAdmin(admin.ModelAdmin):
    """Admin interface for password reset activation codes."""

    list_display = ["user", "activation_code", "created_when"]
    list_filter = ["created_when"]
    search_fields = ["user__username", "user__email", "activation_code"]
    readonly_fields = ["activation_code", "created_when"]
    ordering = ["-created_when"]