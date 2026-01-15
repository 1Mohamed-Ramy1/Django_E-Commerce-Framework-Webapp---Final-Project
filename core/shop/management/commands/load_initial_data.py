"""
Management command to load all initial fixtures at once.

Usage:
    python manage.py load_initial_data
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    """Load all initial data fixtures for the project."""
    
    help = 'Load all initial fixtures (products, categories, coupons, gifts, events, blog)'

    def handle(self, *args, **options):
        """Execute the command."""
        fixtures = [
            ('shop_data', 'Shop data (categories, products, sizes)'),
            ('coupons_data', 'Coupons'),
            ('gift_data', 'Gifts'),
            ('events_data', 'Events'),
            ('blog_data', 'Blog posts'),
        ]

        self.stdout.write(self.style.WARNING('Loading initial data fixtures...'))
        self.stdout.write('')

        for fixture_name, description in fixtures:
            try:
                self.stdout.write(f'Loading {description}... ', ending='')
                call_command('loaddata', fixture_name, verbosity=0)
                self.stdout.write(self.style.SUCCESS('✓'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ ({str(e)})'))

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('Initial data loaded successfully!'))
        self.stdout.write('')
        self.stdout.write('Next steps:')
        self.stdout.write('  1. Create a superuser: python manage.py createsuperuser')
        self.stdout.write('  2. Run the server: python manage.py runserver')
