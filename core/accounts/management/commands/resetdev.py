# accounts/management/commands/resetdev.py
import os
import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.management import call_command
from django.utils import timezone
from django.apps import apps


class Command(BaseCommand):
    help = "Reset sqlite db, run migrations and seed sample data for dev"

    def handle(self, *args, **options):
        db_path = settings.DATABASES['default']['NAME']

        # Delete DB
        if os.path.exists(db_path):
            os.remove(db_path)
            self.stdout.write(self.style.WARNING(f"Deleted DB: {db_path}"))

        self.stdout.write("Running makemigrations/migrate ...")
        call_command('makemigrations')
        call_command('migrate')

        # Import models AFTER migrate
        from django.contrib.auth import get_user_model
        from shop.models import Product
        from events.models import Event
        from weather.models import SearchHistory

        User = get_user_model()

        # ---- Users ----
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
            self.stdout.write(self.style.SUCCESS("Created superuser: admin / adminpass"))

        if not User.objects.filter(username='medo').exists():
            User.objects.create_user('medo', 'medo@example.com', 'medopass')
            self.stdout.write(self.style.SUCCESS("Created normal user: medo / medopass"))

        # ---- Products ----
        if Product.objects.count() == 0:
            Product.objects.create(name="Sample Laptop", price=1500)
            Product.objects.create(name="Sample Phone", price=700)
            Product.objects.create(name="Sample Headphones", price=120)
            self.stdout.write(self.style.SUCCESS("Seeded sample products"))

        # ---- Events ----
        # Ensure the app is installed
        if apps.is_installed('events'):
            Event = apps.get_model('events', 'Event')

            if Event.objects.count() == 0:
                Event.objects.create(
                    name="New Year Sale",
                    event_date=timezone.datetime(2025, 12, 31, 0, 0, tzinfo=timezone.get_current_timezone()),
                    status="approved"
                )

                Event.objects.create(
                    name="Black Friday Deals",
                    event_date=timezone.datetime(2025, 11, 28, 0, 0, tzinfo=timezone.get_current_timezone()),
                    status="running"
                )

                Event.objects.create(
                    name="End of Season Sale",
                    event_date=timezone.datetime.now() + datetime.timedelta(days=10),
                    status="pending"
                )

                self.stdout.write(self.style.SUCCESS("Seeded sample events"))

        # ---- Weather ----
        if SearchHistory.objects.count() == 0:
            SearchHistory.objects.create(city_name="Cairo", temperature=25.0)
            self.stdout.write(self.style.SUCCESS("Seeded sample weather search"))

        self.stdout.write(self.style.SUCCESS(
            "resetdev finished. Login with admin/adminpass or medo/medopass"
        ))
