# core/shop/management/commands/import_json_data.py
import json, os, logging
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.dateparse import parse_datetime
from django.contrib.auth import get_user_model

from shop.models import Product, ProductSize, Order, OrderItem

User = get_user_model()
logger = logging.getLogger('import_json')

SIZE_INDEX_TO_CODE = {0:'XS',1:'S',2:'M',3:'L',4:'XL',5:'XXL'}

class Command(BaseCommand):
    help = "Import users.json, products.json, orders.json from legacy Data folder."

    def add_arguments(self, parser):
        parser.add_argument('--data-dir', type=str, default=os.path.join(settings.BASE_DIR, 'Data'))

    def handle(self, *args, **options):
        data_dir = options['data_dir']
        log_path = os.path.join(settings.BASE_DIR, 'import_log.txt')
        fh = open(log_path, 'a', encoding='utf-8')
        def log(msg):
            fh.write(msg + '\n')
            self.stdout.write(msg)

        # 1) Import users
        users_file = os.path.join(data_dir, 'users.json')
        user_map = {}  # legacy_id -> new_user.pk
        if os.path.exists(users_file):
            with open(users_file, 'r', encoding='utf-8') as f:
                users = json.load(f)
            seen_emails = set()
            for u in users:
                email = (u.get('Email') or '').strip().lower()
                legacy_id = u.get('Id')
                if not email:
                    log(f"[USERS] skip legacy id {legacy_id}: no email")
                    continue
                if email in seen_emails:
                    log(f"[USERS] duplicate email {email} skipped (legacy id {legacy_id})")
                    continue
                username = u.get('Username') or email.split('@')[0]
                password = u.get('Password') or 'changeme'
                is_admin = bool(u.get('IsAdmin'))
                is_warned = bool(u.get('IsWarned'))
                user_obj, created = User.objects.get_or_create(email__iexact=email, defaults={'username':username, 'email':email})
                if created:
                    user_obj.username = username
                    user_obj.email = email
                user_obj.legacy_id = legacy_id
                user_obj.is_staff = is_admin
                user_obj.is_superuser = is_admin
                user_obj.is_warned = is_warned if hasattr(user_obj,'is_warned') else False
                user_obj.set_password(password)
                user_obj.save()
                seen_emails.add(email)
                user_map[legacy_id] = user_obj.pk
                log(f"[USERS] imported {email} -> pk={user_obj.pk}")
        else:
            log("[USERS] file not found, skipping")

        # 2) Import products
        products_file = os.path.join(data_dir, 'products.json')
        product_map = {}
        if os.path.exists(products_file):
            with open(products_file, 'r', encoding='utf-8') as f:
                products = json.load(f)
            for p in products:
                legacy_id = p.get('Id')
                name = p.get('Name') or 'Unnamed'
                category = p.get('Category')
                price = float(p.get('Price') or 0)
                prod, created = Product.objects.get_or_create(legacy_id=legacy_id, defaults={'name':name,'category':category,'price':price})
                if not created:
                    prod.name = name; prod.category = category; prod.price = price; prod.save()
                # sizes
                sizes = p.get('Sizes') or []
                for s in sizes:
                    idx = s.get('Size')
                    qty = s.get('Quantity') or 0
                    try:
                        qty = int(qty)
                    except:
                        qty = 0
                    if qty < 0:
                        log(f"[PRODUCTS] Negative qty for product {legacy_id} size {idx} -> set to 0")
                        qty = 0
                    size_code = SIZE_INDEX_TO_CODE.get(int(idx), 'M')
                    ps, _ = ProductSize.objects.get_or_create(product=prod, size=size_code, defaults={'quantity':qty})
                    if ps.quantity != qty:
                        ps.quantity = qty
                        ps.save()
                product_map[legacy_id] = prod.pk
                log(f"[PRODUCTS] imported {name} (legacy {legacy_id}) -> pk={prod.pk}")
        else:
            log("[PRODUCTS] file not found, skipping")

        # 3) Import orders
        orders_file = os.path.join(data_dir, 'orders.json')
        if os.path.exists(orders_file):
            with open(orders_file, 'r', encoding='utf-8') as f:
                orders = json.load(f)
            for o in orders:
                legacy_id = o.get('Id')
                legacy_userid = o.get('UserId')
                user_pk = user_map.get(legacy_userid)
                user = None
                if user_pk:
                    from django.contrib.auth import get_user_model
                    user = User.objects.filter(pk=user_pk).first()
                payment = o.get('PaymentMethod') or ''
                date_str = o.get('Date')
                try:
                    date = parse_datetime(date_str) if date_str else None
                except:
                    date = None
                order = Order.objects.create(legacy_id=legacy_id, user=user, payment_method=payment, date=date or None)
                items = o.get('Items') or []
                for it in items:
                    prod_legacy = it.get('ProductId')
                    prod_pk = product_map.get(prod_legacy)
                    prod_obj = Product.objects.filter(pk=prod_pk).first() if prod_pk else None
                    qty = int(it.get('Quantity') or 1)
                    size_idx = it.get('Size')
                    size_code = SIZE_INDEX_TO_CODE.get(int(size_idx), 'M')
                    price = prod_obj.price if prod_obj else 0
                    OrderItem.objects.create(order=order, product=prod_obj, size=size_code, quantity=qty, price_at_order=price)
                    # optionally reduce stock (careful: this duplicates real-order semantics)
                    if prod_obj:
                        ps = ProductSize.objects.filter(product=prod_obj, size=size_code).first()
                        if ps:
                            ps.quantity = max(0, ps.quantity - qty)
                            ps.save()
                log(f"[ORDERS] imported order legacy {legacy_id} -> pk={order.pk}")
        else:
            log("[ORDERS] file not found, skipping")

        fh.close()
        log("Import finished. See import_log.txt for details.")
