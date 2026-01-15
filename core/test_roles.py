"""
Test script for user roles and permissions.
Run with: python manage.py shell < test_roles.py
"""

from django.contrib.auth.models import User, Group
from accounts.permissions import (
    get_user_tier, is_admin_user, is_manager_user, 
    is_regular_user, make_user_manager, remove_user_manager
)

print("\n" + "="*60)
print("TESTING USER ROLES AND PERMISSIONS")
print("="*60)

# Test 1: Admin user
print("\n1. Testing Admin User:")
try:
    admin = User.objects.get(username='admin')
    print(f"   ✓ Admin user found: {admin.username}")
    print(f"   ✓ Tier: {get_user_tier(admin)}")
    print(f"   ✓ Is Admin: {is_admin_user(admin)}")
    print(f"   ✓ Superuser: {admin.is_superuser}")
    print(f"   ✓ Staff: {admin.is_staff}")
except User.DoesNotExist:
    print("   ✗ Admin user not found!")

# Test 2: Create test manager
print("\n2. Testing Manager Creation:")
try:
    test_user, created = User.objects.get_or_create(
        username='testmanager',
        defaults={'email': 'testmanager@test.com', 'is_active': True}
    )
    
    if created:
        test_user.set_password('testpass123')
        test_user.save()
        print(f"   ✓ Created test user: {test_user.username}")
    
    # Make manager
    make_user_manager(test_user)
    print(f"   ✓ Promoted to manager")
    print(f"   ✓ Tier: {get_user_tier(test_user)}")
    print(f"   ✓ Is Manager: {is_manager_user(test_user)}")
    print(f"   ✓ Staff: {test_user.is_staff}")
    
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 3: Create test regular user
print("\n3. Testing Regular User:")
try:
    regular_user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'testuser@test.com', 'is_active': True}
    )
    
    if created:
        regular_user.set_password('userpass123')
        regular_user.save()
        print(f"   ✓ Created test user: {regular_user.username}")
    
    print(f"   ✓ Tier: {get_user_tier(regular_user)}")
    print(f"   ✓ Is Regular User: {is_regular_user(regular_user)}")
    print(f"   ✓ Staff: {regular_user.is_staff}")
    
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 4: Manager group
print("\n4. Testing Manager Group:")
try:
    managers_group = Group.objects.get(name='managers')
    print(f"   ✓ Manager group found: {managers_group.name}")
    print(f"   ✓ Permissions count: {managers_group.permissions.count()}")
    print(f"   ✓ Members: {managers_group.user_set.count()}")
except Group.DoesNotExist:
    print("   ✗ Manager group not found!")

# Test 5: Permission checks
print("\n5. Testing Permission Checks:")
print(f"   ✓ Admin is_admin_user: {is_admin_user(admin)}")
print(f"   ✓ Admin is_manager_user: {is_manager_user(admin)}")
print(f"   ✓ Admin is_regular_user: {is_regular_user(admin)}")
print(f"   ✓ Manager is_admin_user: {is_admin_user(test_user)}")
print(f"   ✓ Manager is_manager_user: {is_manager_user(test_user)}")
print(f"   ✓ Manager is_regular_user: {is_regular_user(test_user)}")
print(f"   ✓ User is_admin_user: {is_admin_user(regular_user)}")
print(f"   ✓ User is_manager_user: {is_manager_user(regular_user)}")
print(f"   ✓ User is_regular_user: {is_regular_user(regular_user)}")

# Test 6: Demotion
print("\n6. Testing Manager Demotion:")
try:
    remove_user_manager(test_user)
    test_user.refresh_from_db()
    print(f"   ✓ Demoted manager to user")
    print(f"   ✓ New tier: {get_user_tier(test_user)}")
    print(f"   ✓ Is Regular User: {is_regular_user(test_user)}")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "="*60)
print("✓ ALL TESTS COMPLETED")
print("="*60 + "\n")
