"""
Permission classes and decorators for role-based access control.

Implements three-tier user hierarchy:
- ADMIN: Full system access (ELOSTORA)
- MANAGER: Staff access with limited user management
- USER: Standard user with no admin privileges
"""
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied


class UserTier:
    """User tier constants."""
    ADMIN = 'admin'
    MANAGER = 'manager'
    USER = 'user'


def get_user_tier(user):
    """
    Determine user's tier level.
    
    Returns:
        str: One of UserTier.ADMIN, UserTier.MANAGER, UserTier.USER
    """
    if not user.is_active:
        return UserTier.USER
    
    # Check if user is admin (ELOSTORA or any with username 'admin')
    if user.is_superuser or user.username.lower() in ['admin', 'elostora']:
        return UserTier.ADMIN
    
    # Check if user is staff (manager) - any staff user is a manager
    if user.is_staff:
        return UserTier.MANAGER
    
    return UserTier.USER


def is_admin_user(user):
    """Check if user is admin tier."""
    return get_user_tier(user) == UserTier.ADMIN


def is_manager_user(user):
    """Check if user is manager tier."""
    return get_user_tier(user) == UserTier.MANAGER


def is_regular_user(user):
    """Check if user is regular user tier."""
    return get_user_tier(user) == UserTier.USER


def setup_user_groups():
    """
    Create user groups for role-based access control.
    Run this once to initialize groups.
    """
    # Create manager group
    managers_group, created = Group.objects.get_or_create(name='managers')
    
    # Add permissions to managers group
    user_content_type = ContentType.objects.get_for_model(User)
    permissions = Permission.objects.filter(
        content_type=user_content_type,
        codename__in=['add_user', 'change_user', 'delete_user', 'view_user']
    )
    managers_group.permissions.set(permissions)
    
    return managers_group, created


def create_or_get_admin(username='admin', email='admin@8080@', password='admin@8080@'):
    """
    Create or get the admin user.
    
    Args:
        username (str): Admin username
        email (str): Admin email
        password (str): Admin password
    
    Returns:
        User: Admin user instance
    """
    admin_user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': email,
            'is_superuser': True,
            'is_staff': True,
            'is_active': True,
            'first_name': 'System',
            'last_name': 'Administrator'
        }
    )
    
    if created or not admin_user.check_password(password):
        admin_user.set_password(password)
        admin_user.is_superuser = True
        admin_user.is_staff = True
        admin_user.is_active = True
        admin_user.save()
    
    return admin_user, created


def make_user_manager(user):
    """
    Promote a user to manager tier.
    
    Args:
        user (User): User to promote
    """
    if not user.is_staff:
        user.is_staff = True
        user.save()
    
    managers_group = Group.objects.get(name='managers')
    user.groups.add(managers_group)


def remove_user_manager(user):
    """
    Demote a manager back to regular user.
    
    Args:
        user (User): Manager to demote
    """
    managers_group = Group.objects.get(name='managers')
    user.groups.remove(managers_group)
    
    # Only remove is_staff if no other groups need it
    if user.groups.count() == 0:
        user.is_staff = False
        user.save()
