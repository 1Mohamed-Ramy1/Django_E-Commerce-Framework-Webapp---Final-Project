from django.core.management.base import BaseCommand
from shop.models import Category, Subcategory, Product, ProductSize, SIZE_CHOICES
import random

class Command(BaseCommand):
    help = 'Populate products with real, diverse product names for each category'

    def handle(self, *args, **kwargs):
        self.stdout.write('🚀 Starting to populate with realistic products...\n')

        # Real product names for each category and subcategory
        products_data = {
            'Amazon Devices & Accessories': {
                'Echo Devices': [
                    'Echo Dot 5th Gen', 'Echo Show 15', 'Echo Studio', 'Echo Flex', 'Echo Pop',
                    'Echo Sub Wireless Subwoofer', 'Echo Auto', 'Echo Buds Pro', 'Echo Frames Smart Glasses',
                    'Echo Glow Night Light', 'Echo Hub', 'Echo Input Compact Speaker', 'Echo Link Wireless',
                    'Echo Spot', 'Echo Device Stand', 'Echo Dot Wall Mount', 'Echo Rubber Bumper'
                ],
                'Fire Tablets': [
                    'Fire Max 11 Tablet', 'Fire HD 8 Tablet', 'Fire HD 10 Tablet', 'Fire 7 Tablet',
                    'Fire Tablet Keyboard Case', 'Fire Tablet Stand', 'Fire Tablet Screen Protector',
                    'Fire Tablet Charging Cable', 'Fire Tablet Power Adapter', 'Fire Tablet Kids Case'
                ],
                'Kindle E-readers': [
                    'Kindle Paperwhite 2024', 'Kindle Oasis', 'Kindle Scribe', 'Kindle Basic',
                    'Kindle Colorsoft', 'Kindle Case Leather', 'Kindle Screen Protector', 'Kindle Reading Light',
                    'Kindle Battery Pack', 'Kindle USB-C Cable'
                ],
                'Fire TV': [
                    'Fire TV Stick 4K', 'Fire TV Cube', 'Fire TV Stick Lite', 'Fire TV Omni Series',
                    'Fire TV Remote Control', 'Fire TV HDMI Cable', 'Fire TV Power Cable'
                ],
                'Accessories': [
                    'Echo Device Mount', 'Amazon Basics HDMI Cable', 'Amazon Basics USB Cable',
                    'Amazon Smart Plug', 'Smart Home Hub', 'WiFi Extender'
                ]
            },
            'Appliances': {
                'Large Appliances': [
                    'LG French Door Refrigerator', 'Samsung Washing Machine', 'Whirlpool Dryer',
                    'GE Electric Range', 'Frigidaire Dishwasher', 'KitchenAid Refrigerator',
                    'Maytag Washer Combo', 'LG Gas Range', 'Samsung French Door Fridge'
                ],
                'Small Appliances': [
                    'Instant Pot Duo', 'Ninja Blender', 'Cuisinart Coffee Maker', 'Philips Air Fryer',
                    'Breville Toaster Oven', 'KitchenAid Mixer', 'Ninja Food Processor', 'Hamilton Beach Blender',
                    'Crockpot Slow Cooker', 'Vitamix Blender', 'Nespresso Coffee Machine'
                ],
                'Heating & Cooling': [
                    'Dyson Space Heater', 'Lasko Tower Fan', 'Honeywell Air Purifier', 'LG Air Conditioner',
                    'Frigidaire Portable AC', 'Vornado Heater', 'Levoit Air Purifier'
                ],
                'Vacuums': [
                    'Dyson V15 Vacuum', 'Roomba j7+ Robot Vacuum', 'Shark Navigator Vacuum',
                    'Bissell CrossWave', 'Hoover Linx Vacuum', 'Tineco Smart Vacuum'
                ],
                'Kitchen Appliances': [
                    'Microwave Oven', 'Coffee Grinder', 'Egg Cooker', 'Rice Cooker', 'Waffle Maker',
                    'Panini Press', 'Sandwich Maker', 'Electric Kettle'
                ]
            },
            'Electronics': {
                'Laptops': [
                    'MacBook Pro 16\" M3 Max', 'Dell XPS 15', 'HP Pavilion 15', 'Lenovo ThinkPad X1',
                    'ASUS VivoBook', 'Acer Aspire 5', 'MSI GS66 Gaming Laptop', 'ROG Strix Gaming Laptop',
                    'Surface Laptop 6', 'HP Spectre x360'
                ],
                'Desktops': [
                    'Apple iMac 24"', 'Dell XPS Desktop', 'HP Envy Desktop', 'ASUS ROG Desktop',
                    'Corsair Vengeance Gaming PC', 'Alienware Aurora Desktop', 'Lenovo IdeaCentre'
                ],
                'Tablets': [
                    'iPad Air 2024', 'iPad Pro 12.9"', 'Samsung Galaxy Tab S9', 'Microsoft Surface Pro',
                    'Lenovo Tab M10', 'Amazon Fire Max 11'
                ],
                'Cameras': [
                    'Canon EOS R6', 'Sony A7IV', 'Nikon D850', 'GoPro Hero 12', 'DJI Air 3S',
                    'Fujifilm X-T5', 'Canon PowerShot G7X', 'Panasonic Lumix S5'
                ],
                'TVs': [
                    'LG OLED 55"', 'Samsung QN90D', 'Sony Bravia K95XR', 'TCL 85" 4K', 'Hisense U8H',
                    'Vizio M-Series', 'LG NanoCell 65"'
                ],
                'Audio Equipment': [
                    'Sony WH-1000XM5 Headphones', 'Bose QuietComfort 45', 'Apple AirPods Pro Max',
                    'Sennheiser Momentum 4', 'Beats Studio Pro', 'JBL Flip 6 Speaker', 'Sonos Arc'
                ]
            },
            'Clothing, Shoes & Jewelry': {
                'Men': [
                    'Oxford Button-Down Shirt', 'Crewneck T-Shirt', 'Polo Shirt', 'V-Neck Sweater',
                    'Hooded Sweatshirt', 'Cargo Pants', 'Dress Pants', 'Chino Shorts',
                    'Fleece Jacket', 'Denim Jacket', 'Wool Blazer', 'Cardigan Sweater'
                ],
                'Women': [
                    'Floral Blouse', 'Casual Tank Top', 'Wrap Dress', 'Maxi Skirt',
                    'Denim Shorts', 'Leggings', 'Yoga Pants', 'Blazer Jacket',
                    'Sweater Dress', 'Cardigan', 'Striped Shirt', 'Linen Pants'
                ],
                'Kids': [
                    'Kids T-Shirt', 'Child Jeans', 'Hoodie', 'Shorts', 'Dress',
                    'Romper', 'Jacket', 'Leggings', 'Polo Shirt'
                ],
                'Shoes': [
                    'Nike Air Max', 'Adidas Ultraboost', 'New Balance 990', 'Converse Chuck Taylors',
                    'Vans Old Skool', 'Dr. Martens Boots', 'Timberland Boots', 'Cole Haan Loafers',
                    'Clarks Desert Boot', 'Puma Suede', 'Asics Gel-Lyte'
                ],
                'Jewelry': [
                    'Gold Chain Necklace', 'Diamond Ring', 'Pearl Earrings', 'Silver Bracelet',
                    'Leather Watch', 'Gold Bangle', 'Pendant Necklace', 'Stud Earrings',
                    'Cocktail Ring', 'Tennis Bracelet'
                ]
            },
            'Books': {
                'Fiction': [
                    'The Great Gatsby', 'To Kill a Mockingbird', 'Pride and Prejudice', '1984',
                    'The Hobbit', 'Dune', 'The Lord of the Rings', 'Harry Potter Box Set',
                    'The Midnight Library', 'Educated', 'The Silent Patient', 'The Woman in Cabin 10'
                ],
                'Non-Fiction': [
                    'Sapiens', 'Atomic Habits', 'Thinking, Fast and Slow', 'Educated',
                    'The Art of War', "Man's Search for Meaning", 'Outliers', 'Mindset'
                ],
                'Textbooks': [
                    'College Algebra', 'Calculus for Beginners', 'Organic Chemistry Guide', 'Physics Principles',
                    'World History Timeline', 'Biology Essentials', 'Psychology Today'
                ],
                'Children Books': [
                    'Where the Wild Things Are', "Charlotte's Web", 'The Very Hungry Caterpillar',
                    'Winnie the Pooh', 'Curious George', 'The Tale of Despereaux'
                ],
                'Comics & Graphic Novels': [
                    'Batman: The Dark Knight Returns', 'Watchmen', 'The Sandman', 'X-Men Omnibus',
                    'Spider-Man Collection', 'Wonder Woman Series'
                ]
            },
            'Cell Phones & Accessories': {
                'Smartphones': [
                    'iPhone 15 Pro Max', 'Samsung Galaxy S24', 'Google Pixel 8 Pro', 'OnePlus 12',
                    'Motorola Edge 50', 'Nothing Phone', 'Realme GT', 'Xiaomi 14'
                ],
                'Cases & Covers': [
                    'OtterBox Defender Case', 'Spigen Tough Armor Case', 'Lifeproof Waterproof Case',
                    'Casetify iPhone Case', 'Nomad Rugged Case', 'Tech21 Evo Case'
                ],
                'Chargers': [
                    'Anker Fast Charger', 'Belkin USB-C Charger', 'Apple MagSafe Charger',
                    'Mophie Wireless Charger', 'AUKEY PD Charger', 'RAVPower Charger'
                ],
                'Screen Protectors': [
                    'Tempered Glass Screen Protector', 'Anti-Glare Screen Protector',
                    'Privacy Screen Protector', 'Gorilla Glass Protector'
                ],
                'Headphones': [
                    'AirPods Pro 2', 'Sony WF-1000XM4', 'Google Pixel Buds Pro', 'Samsung Galaxy Buds2',
                    'Jabra Elite 85t', 'Nothing Ear'
                ]
            },
            'Home & Kitchen': {
                'Furniture': [
                    'Sofa Sectional', 'Dining Table Set', 'Desk Chair', 'Bookshelf', 'Coffee Table',
                    'Bed Frame', 'Nightstand', 'Dresser', 'Office Desk', 'Bar Stool'
                ],
                'Bedding': [
                    'Sheet Set Queen', 'Comforter Set', 'Pillows Memory Foam', 'Mattress Protector',
                    'Duvet Cover', 'Bed Skirt', 'Pillowcase Set'
                ],
                'Kitchen Utensils': [
                    'Knife Set', 'Cutting Board', 'Mixing Bowls', 'Measuring Cups', 'Wooden Spoons',
                    'Silicone Spatulas', 'Whisk', 'Tongs', 'Can Opener', 'Grater'
                ],
                'Storage': [
                    'Storage Bins', 'Shelving Unit', 'Closet Organizer', 'Drawer Dividers',
                    'Vacuum Storage Bags', 'Under-Bed Storage'
                ],
                'Home Decor': [
                    'Wall Art Canvas', 'Throw Pillows', 'Area Rug', 'Mirror', 'Lamp',
                    'Wall Clock', 'Plants', 'Curtains', 'Wall Stickers', 'Frames'
                ]
            },
            'Sports & Outdoors': {
                'Exercise Equipment': [
                    'Dumbbells Set', 'Yoga Mat', 'Resistance Bands', 'Treadmill', 'Exercise Bike',
                    'Kettlebell', 'Pull-Up Bar', 'Weight Bench', 'Jump Rope'
                ],
                'Camping': [
                    'Tent 4-Person', 'Sleeping Bag', 'Camping Stove', 'Backpack 60L', 'Camping Pillow',
                    'Lantern', 'Rope', 'Tent Stakes', 'Cooler'
                ],
                'Cycling': [
                    'Mountain Bike', 'Road Bike', 'Bike Helmet', 'Bike Lock', 'Bike Light',
                    'Bike Pump', 'Handlebar Grips', 'Pedals'
                ],
                'Water Sports': [
                    'Surfboard', 'Snorkel Set', 'Paddleboard', 'Wetsuit', 'Swim Goggles',
                    'Swim Fins', 'Kickboard'
                ],
                'Team Sports': [
                    'Basketball', 'Soccer Ball', 'Football', 'Volleyball', 'Baseball Glove',
                    'Tennis Racket', 'Badminton Set', 'Hockey Stick'
                ]
            },
            'Toys & Games': {
                'Action Figures': [
                    'Marvel Legends Iron Man', 'DC Comics Batman', 'Star Wars Yoda', 'Funko Pop Figures',
                    'Transformers Optimus Prime', 'LEGO Minifigures', 'My Little Pony Figures'
                ],
                'Dolls': [
                    'Barbie Doll Classic', 'American Girl Doll', 'LOL Surprise Doll', 'Baby Alive Doll',
                    'Cabbage Patch Kid'
                ],
                'Board Games': [
                    'Monopoly', 'Scrabble', 'Catan Board Game', 'Ticket to Ride', 'Carcassonne',
                    'Pandemic', 'Codenames', 'Risk'
                ],
                'Building Toys': [
                    'LEGO City Set', 'LEGO Star Wars Set', 'LEGO Harry Potter', 'Mega Construx',
                    "K'NEX Building System", 'Marble Run Set'
                ],
                'Educational Toys': [
                    'Science Kit', 'Puzzle 1000 Piece', 'STEM Robot Kit', 'Microscope Set',
                    'Crystal Growing Kit', 'Model Rocket'
                ]
            },
            'Beauty & Personal Care': {
                'Makeup': [
                    'Foundation', 'Concealer', 'Blush', 'Eyeshadow Palette', 'Mascara',
                    'Lipstick', 'Eyeliner', 'Primer', 'Setting Spray'
                ],
                'Skincare': [
                    'Moisturizer', 'Cleanser', 'Toner', 'Face Serum', 'Eye Cream',
                    'Face Mask', 'Exfoliant', 'Sunscreen'
                ],
                'Hair Care': [
                    'Shampoo', 'Conditioner', 'Hair Mask', 'Hair Oil', 'Hair Serum',
                    'Dry Shampoo', 'Hair Spray'
                ],
                'Fragrances': [
                    'Perfume Women', 'Cologne Men', 'Body Spray', 'Room Spray', 'Candles'
                ],
                'Personal Care': [
                    'Toothbrush Electric', 'Toothpaste', 'Dental Floss', 'Mouthwash', 'Deodorant',
                    'Body Wash', 'Lotion', 'Razor'
                ]
            },
            'Music & Entertainment': {
                'Pop Music': [
                    'Dua Lipa Album', 'The Weeknd Album', 'Taylor Swift Album', 'Ariana Grande Album',
                    'Billie Eilish Album', 'Harry Styles Album'
                ],
                'Rock': [
                    'The Beatles Collection', 'Pink Floyd Album', 'Queen Album', 'Led Zeppelin Album',
                    'Rolling Stones Album', 'David Bowie Album'
                ],
                'Classical': [
                    'Beethoven Symphony', 'Mozart Collection', 'Bach Classics', 'Vivaldi Four Seasons',
                    'Chopin Nocturnes', 'Debussy Piano Works'
                ],
                'Jazz': [
                    'Miles Davis Kind of Blue', 'John Coltrane Album', 'Duke Ellington Collection',
                    'Chet Baker Album'
                ],
                'Vinyl Records': [
                    'Vinyl Player Turntable', 'Record Sleeves', 'Vinyl Brush Cleaner', 'Stylus Needles',
                    'Record Stand'
                ]
            },
            'Video Games': {
                'PlayStation': [
                    'God of War Ragnarok', 'Elden Ring', 'Spider-Man 2', 'Final Fantasy XVI',
                    'Gran Turismo 7', 'Ghostwire Tokyo', 'Resident Evil 4 Remake'
                ],
                'Xbox': [
                    'Starfield', 'Forza Motorsport', 'Halo Infinite', 'Gears 5', 'Xbox Game Pass'
                ],
                'Nintendo': [
                    'The Legend of Zelda', 'Super Mario Bros', 'Pokemon Scarlet Violet', 'Animal Crossing',
                    'Mario Kart 8', 'Super Smash Bros'
                ],
                'PC Games': [
                    'Cyberpunk 2077', 'The Witcher 3', 'Valorant', 'Counter-Strike 2', 'DOTA 2',
                    "Baldur's Gate 3"
                ],
                'Gaming Accessories': [
                    'Gaming Mouse', 'Mechanical Keyboard', 'Gaming Headset', 'Controller', 'Game Pad',
                    'Joystick', 'Charging Dock'
                ]
            },
        }

        # Clear existing products
        self.stdout.write(self.style.WARNING('\n⚠️  Clearing existing products...\n'))
        Product.objects.all().delete()

        total_products = 0
        
        for cat_name, subcats_dict in products_data.items():
            self.stdout.write(f'\n📂 Creating category: {cat_name}')
            
            # Get or create category
            category = Category.objects.filter(name=cat_name).first()
            if not category:
                category = Category.objects.create(
                    name=cat_name,
                    description=f'Browse our extensive collection of {cat_name.lower()} products'
                )
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created category: {cat_name}'))
            else:
                self.stdout.write(f'  ↻ Using existing category: {cat_name}')
            
            # Create products for each subcategory
            for subcat_name, product_names in subcats_dict.items():
                # Get subcategory
                subcategory = Subcategory.objects.filter(category=category, name=subcat_name).first()
                
                self.stdout.write(f'    ├─ {subcat_name}: {len(product_names)} products')
                
                for product_name in product_names:
                    # Random price
                    price = round(random.uniform(9.99, 999.99), 2)
                    stock = random.randint(5, 200)
                    
                    product, created = Product.objects.get_or_create(
                        name=product_name,
                        defaults={
                            'category_ref': category,
                            'subcategory': subcategory,
                            'price': price,
                            'stock': stock,
                            'description': f'{product_name} - High quality {subcat_name.lower()} from {cat_name}',
                            'short_description': f'{product_name} - ${price}'
                        }
                    )
                    
                    if created:
                        # Add product sizes
                        if 'Clothing' in cat_name or 'Shoes' in cat_name:
                            for size_code, _ in SIZE_CHOICES:
                                ProductSize.objects.get_or_create(
                                    product=product,
                                    size=size_code,
                                    defaults={'quantity': random.randint(3, 50)}
                                )
                        else:
                            ProductSize.objects.get_or_create(
                                product=product,
                                size='M',
                                defaults={'quantity': stock}
                            )
                        total_products += 1
        
        # Summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'\n🎉 Real products population complete!'))
        self.stdout.write(self.style.SUCCESS(f'  ├─ Categories: {Category.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'  ├─ Subcategories: {Subcategory.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'  ├─ Products: {Product.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'  └─ Total new products: {total_products}'))
        self.stdout.write('\n' + '='*60 + '\n')
