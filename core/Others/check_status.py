import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from shop.models import Product

samples = [
    'Fire Tablet Power Adapter',
    'Fire Tablet Charging Cable', 
    'Fire Tablet Screen Protector',
]

print('Current product images:')
print('=' * 70)
for name in samples:
    p = Product.objects.filter(name__icontains=name.split()[-2]).first()
    if p:
        print(f'{p.name[:45]:<45} | {p.image[:50]}...')
    else:
        print(f'{name}: Not found')
