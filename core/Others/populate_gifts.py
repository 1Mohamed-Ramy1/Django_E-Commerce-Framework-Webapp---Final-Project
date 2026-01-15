#!/usr/bin/env python
"""Populate database with 10 premium gift items"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from gift.models import Gift

# Clear existing gifts
Gift.objects.all().delete()

# Premium gift data (10k-50k points range)
gifts_data = [
    {
        'name': 'Apple AirPods Pro (2nd Gen)',
        'description': 'Active Noise Cancellation, Adaptive Audio, and Personalized Spatial Audio with dynamic head tracking.',
        'points_cost': 12000,
        'stock_quantity': 100,
    },
    {
        'name': 'Samsung Galaxy Watch 6',
        'description': 'Advanced health monitoring, sleep tracking, and fitness features in a premium smartwatch design.',
        'points_cost': 15000,
        'stock_quantity': 80,
    },
    {
        'name': 'Sony WH-1000XM5 Headphones',
        'description': 'Industry-leading noise cancellation with exceptional sound quality and 30-hour battery life.',
        'points_cost': 18000,
        'stock_quantity': 90,
    },
    {
        'name': 'iPad Air (5th Generation)',
        'description': '10.9-inch Liquid Retina display, M1 chip, and support for Apple Pencil and Magic Keyboard.',
        'points_cost': 25000,
        'stock_quantity': 60,
    },
    {
        'name': 'Nintendo Switch OLED',
        'description': 'Vibrant 7-inch OLED screen, enhanced audio, and 64GB of internal storage for gaming on the go.',
        'points_cost': 16000,
        'stock_quantity': 75,
    },
    {
        'name': 'DJI Mini 3 Pro Drone',
        'description': '4K HDR video, 34-minute flight time, and intelligent features for stunning aerial photography.',
        'points_cost': 30000,
        'stock_quantity': 50,
    },
    {
        'name': 'Dyson V15 Detect Cordless Vacuum',
        'description': 'Laser dust detection and powerful suction with up to 60 minutes of run time.',
        'points_cost': 28000,
        'stock_quantity': 65,
    },
    {
        'name': 'PlayStation 5 Console',
        'description': 'Next-gen gaming with ultra-high speed SSD, ray tracing, and immersive 4K gaming experience.',
        'points_cost': 35000,
        'stock_quantity': 55,
    },
    {
        'name': 'MacBook Air M2',
        'description': '13.6-inch Liquid Retina display, powerful M2 chip, and all-day battery life in a sleek design.',
        'points_cost': 50000,
        'stock_quantity': 3,
    },
    {
        'name': 'Bose SoundLink Revolve+ II',
        'description': 'Portable Bluetooth speaker with 360-degree sound and up to 17 hours of battery life.',
        'points_cost': 10000,
        'stock_quantity': 120,
    },
]

# Create gifts
created_count = 0
for gift_data in gifts_data:
    gift = Gift.objects.create(**gift_data)
    created_count += 1
    print(f"✓ Created: {gift.name} - {gift.points_cost:,} points")

print(f"\n🎉 Successfully created {created_count} premium gifts!")
print(f"Total points range: 10,000 - 50,000")
