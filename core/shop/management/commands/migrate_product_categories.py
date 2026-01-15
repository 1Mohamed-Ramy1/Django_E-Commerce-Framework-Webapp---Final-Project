from django.core.management.base import BaseCommand
from django.db import transaction

from shop.models import Product, Category


class Command(BaseCommand):
    help = "Migrate Product.category (text) to Product.category_ref (FK) and ensure categories exist."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Do not write any changes, only report what would happen.",
        )

    def handle(self, *args, **options):
        dry_run = options.get("dry_run", False)

        qs = Product.objects.filter(category_ref__isnull=True).exclude(category__isnull=True).exclude(category="")
        total = qs.count()
        created_cats = 0
        updated_products = 0

        self.stdout.write(self.style.NOTICE(f"Scanning {total} products missing category_ref..."))

        @transaction.atomic
        def run():
            nonlocal created_cats, updated_products
            for p in qs.iterator():
                cat_name = p.category.strip()
                category_obj, created = Category.objects.get_or_create(name=cat_name)
                if created:
                    created_cats += 1
                p.category_ref = category_obj
                p.save(update_fields=["category_ref"])
                updated_products += 1

        if dry_run:
            self.stdout.write("Dry run: no database changes will be made.")
            # Wrap in rollback transaction
            with transaction.atomic():
                run()
                transaction.set_rollback(True)
        else:
            run()

        self.stdout.write(self.style.SUCCESS(
            f"Done. Categories created: {created_cats}, Products updated: {updated_products}."
        ))
