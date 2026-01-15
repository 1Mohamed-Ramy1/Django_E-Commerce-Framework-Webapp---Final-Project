"""Test sending activation code email."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from accounts.models import PasswordReset, User
from django.core.mail import EmailMessage
from django.conf import settings

print("=" * 60)
print("Testing Activation Code Email")
print("=" * 60)

# Get admin user or first user
try:
    user = User.objects.first()
    if not user:
        print("✗ No users found in database")
        exit(1)
    print(f"✓ Using user: {user.username} ({user.email})")
except Exception as e:
    print(f"✗ Error getting user: {e}")
    exit(1)

# Delete old resets
PasswordReset.objects.filter(user=user).delete()

# Create new reset
reset = PasswordReset(user=user)
reset.save()

print(f"\n✓ Generated activation code: {reset.activation_code}")
print(f"  Created at: {reset.created_when}")

print("\n" + "=" * 60)
print("Sending Email")
print("=" * 60)

try:
    email = EmailMessage(
        'Password Reset - Activation Code',
        f'Your password reset activation code is:\n\n{reset.activation_code}\n\nThis code will expire in 10 minutes.\nEnter this code on the password reset page to continue.',
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_HOST_USER]  # Send to yourself for testing
    )
    email.send(fail_silently=False)
    print(f"✓ Email sent successfully to {settings.EMAIL_HOST_USER}")
    print(f"\nEmail Content:")
    print("-" * 60)
    print(f"Subject: Password Reset - Activation Code")
    print(f"To: {settings.EMAIL_HOST_USER}")
    print(f"Body:\nYour password reset activation code is:\n\n{reset.activation_code}\n\nThis code will expire in 10 minutes.\nEnter this code on the password reset page to continue.")
    print("-" * 60)
except Exception as e:
    print(f"✗ Error sending email: {e}")

# Cleanup
reset.delete()
print("\n✓ Test completed and cleaned up")
print("\n📧 Check your inbox at:", settings.EMAIL_HOST_USER)
