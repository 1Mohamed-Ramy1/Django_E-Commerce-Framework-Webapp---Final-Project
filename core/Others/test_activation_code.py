"""Test the new activation code system."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from accounts.models import PasswordReset, User
from django.utils import timezone

print("=" * 50)
print("Testing Activation Code System")
print("=" * 50)

# Get or create a test user
try:
    user = User.objects.get(username='testuser')
    print(f"✓ Found test user: {user.username} ({user.email})")
except User.DoesNotExist:
    print("⚠ Test user not found. Creating one...")
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    print(f"✓ Created test user: {user.username} ({user.email})")

print("\n" + "=" * 50)
print("Creating Password Reset Request")
print("=" * 50)

# Create password reset
reset = PasswordReset(user=user)
reset.save()

print(f"✓ Password reset created")
print(f"  User: {reset.user.username}")
print(f"  Activation Code: {reset.activation_code}")
print(f"  Created: {reset.created_when}")
print(f"  Code length: {len(reset.activation_code)} digits")

# Verify code format
if len(reset.activation_code) == 6 and reset.activation_code.isdigit():
    print("✓ Code format is correct (6 digits)")
else:
    print("✗ Code format is incorrect!")

print("\n" + "=" * 50)
print("Testing Code Retrieval")
print("=" * 50)

# Test retrieval
try:
    retrieved = PasswordReset.objects.get(activation_code=reset.activation_code)
    print(f"✓ Successfully retrieved reset by code: {retrieved.activation_code}")
    print(f"  Belongs to: {retrieved.user.username}")
except PasswordReset.DoesNotExist:
    print("✗ Failed to retrieve reset by code")

print("\n" + "=" * 50)
print("Testing Expiration Check")
print("=" * 50)

# Test expiration
expiry_time = reset.created_when + timezone.timedelta(minutes=10)
time_left = (expiry_time - timezone.now()).total_seconds() / 60
print(f"  Code expires at: {expiry_time}")
print(f"  Time left: {time_left:.1f} minutes")

if timezone.now() < expiry_time:
    print("✓ Code is still valid")
else:
    print("✗ Code has expired")

print("\n" + "=" * 50)
print("Testing Multiple Codes")
print("=" * 50)

# Create 5 more resets to test uniqueness
codes = [reset.activation_code]
for i in range(5):
    temp_reset = PasswordReset(user=user)
    temp_reset.save()
    codes.append(temp_reset.activation_code)
    temp_reset.delete()

print(f"✓ Generated {len(codes)} codes")
print(f"  Codes: {', '.join(codes)}")
print(f"  Unique codes: {len(set(codes))}")

if len(set(codes)) == len(codes):
    print("✓ All codes are unique")
else:
    print("✗ Duplicate codes found!")

# Cleanup
reset.delete()
print("\n✓ Test completed and cleaned up")
