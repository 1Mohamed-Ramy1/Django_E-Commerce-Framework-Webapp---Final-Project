#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.core.management import call_command

try:
    call_command('migrate', 'weather', '--noinput', verbosity=2)
    print("\n✓ Weather migrations applied successfully!")
except Exception as e:
    print(f"\n✗ Migration error: {e}")
    sys.exit(1)
