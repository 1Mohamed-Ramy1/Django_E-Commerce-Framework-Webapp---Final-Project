"""Test email configuration."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.core.mail import EmailMessage
from django.conf import settings

print("Email Configuration:")
print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
print(f"EMAIL_HOST_PASSWORD: {'*' * 10} (hidden)")
print("\nAttempting to send test email...")

try:
    email = EmailMessage(
        'Test Email',
        'This is a test email from your Django app.',
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_HOST_USER]  # Send to yourself
    )
    email.send(fail_silently=False)
    print("✓ Email sent successfully!")
except Exception as e:
    print(f"✗ Error sending email: {e}")
    print("\nTroubleshooting tips:")
    print("1. Make sure you're using an App Password, not your regular Gmail password")
    print("2. Enable 2-factor authentication on your Gmail account")
    print("3. Generate an App Password at: https://myaccount.google.com/apppasswords")
    print("4. Update EMAIL_PASS in your .env file with the App Password")
