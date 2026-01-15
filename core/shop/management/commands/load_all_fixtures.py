"""
Management command to load all fixtures data at once.
This command loads initial data for products, categories, blog posts, events, gifts, and coupons.
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Load all initial fixtures data (products, blog, events, gifts, coupons)'

    def handle(self, *args, **options):
        fixtures = [
            ('products', 'Products, Categories, and SubCategories'),
            ('blog_data', 'Blog Posts and Categories'),
            ('events_data', 'Events'),
            ('gifts_data', 'Gift Rewards'),
            ('coupons_data', 'Coupons'),
        ]

        self.stdout.write(self.style.WARNING('Loading all fixtures data...'))
        self.stdout.write('')

        for fixture_name, description in fixtures:
            try:
                self.stdout.write(f'Loading {description}...', ending=' ')
                call_command('loaddata', fixture_name, verbosity=0)
                self.stdout.write(self.style.SUCCESS('✓'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Error: {e}'))

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('Successfully loaded all fixtures!'))
        self.stdout.write('')
        self.stdout.write('Next steps:')
        self.stdout.write('  1. Create a superuser: python manage.py createsuperuser')
        self.stdout.write('  2. Run the server: python manage.py runserver')
