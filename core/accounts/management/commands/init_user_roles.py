"""Management command to initialize user roles and permissions."""
from django.core.management.base import BaseCommand
from accounts.permissions import setup_user_groups, create_or_get_admin


class Command(BaseCommand):
    help = 'Initialize user roles and permissions (Admin, Manager, User hierarchy)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Reset and recreate all groups',
        )

    def handle(self, *args, **options):
        self.stdout.write('Initializing user roles hierarchy...')
        
        # Setup groups
        managers_group, created = setup_user_groups()
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'✓ Created "managers" group')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'✓ "managers" group already exists')
            )
        
        # Create admin user
        admin_user, created = create_or_get_admin()
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'✓ Created admin user: {admin_user.username}')
            )
            self.stdout.write(f'  Email: {admin_user.email}')
            self.stdout.write(f'  Password: Use the one provided during setup')
        else:
            self.stdout.write(
                self.style.WARNING(f'✓ Admin user already exists: {admin_user.username}')
            )
        
        self.stdout.write(self.style.SUCCESS('\n✓ User hierarchy initialized successfully!'))
        self.stdout.write('\nUser Tiers:')
        self.stdout.write('  👑 ADMIN - Full system access (ELOSTORA)')
        self.stdout.write('  ⭐ MANAGER - Staff access with limited user management')
        self.stdout.write('  👤 USER - Standard user')
