from django.core.management.base import BaseCommand
from shop.models import Category, Subcategory, Product, ProductSize, SIZE_CHOICES
import random
import uuid

class Command(BaseCommand):
    help = 'Add relevant products to all categories (preserves existing products)'

    def handle(self, *args, **kwargs):
        self.stdout.write('🚀 Starting to add products to all categories...\n')

        # Comprehensive product catalogs by category
        category_products = {
            'Arts, Crafts & Sewing': {
                'Painting Supplies': [
                    'Acrylic Paint Set', 'Watercolor Palette Premium', 'Oil Paint Tubes Collection', 'Paint Brushes Professional',
                    'Canvas Painting Pad', 'Sketching Pencil Set', 'Charcoal Drawing Set', 'Pastel Colors Assortment',
                    'Paint Mixing Palette', 'Fine Art Easel', 'Professional Brush Set', 'Watercolor Blocks',
                    'Acrylic Paint Starter Kit', 'Artist Sketchbook Premium', 'Blending Brushes Set', 'Paint Thinner Solution',
                    'Color Mixing Guide', 'Paint Palette Knife', 'Canvas Board Pack', 'Brush Cleaner Solution',
                    'Spray Paint Colors', 'Gesso Primer', 'Varnish Gloss', 'Matte Varnish', 'Extra Fine Brushes',
                    'Bristle Brushes Set', 'Sable Brushes Premium', 'Canvas Stretched', 'Wood Easel Stand',
                    'Paint Holder Organizer', 'Brush Storage Case', 'Paint Thinner Odorless', 'Mineral Spirits',
                    'Linseed Oil Medium', 'Turpentine Solution', 'Acrylic Primer', 'Paint Mixing Mediums',
                    'High Flow Acrylic', 'Heavy Body Paint', 'Metallic Paint Set', 'Fluorescent Paint Colors'
                ],
                'Sewing': [
                    'Sewing Machine Digital', 'Thread Assortment Pack', 'Sewing Needle Set', 'Fabric Scissors Professional',
                    'Sewing Machine Needles', 'Bobbin Thread Pack', 'Embroidery Hoop Set', 'Thimble Set',
                    'Sewing Tape Measure', 'Fabric Pins Box', 'Seam Ripper Tool', 'Pincushion Decorative',
                    'Buttonhole Foot Attachment', 'Presser Feet Set', 'Sewing Pattern Book', 'Fabric Marking Pen',
                    'Thread Organizer', 'Needle Storage Box', 'Sewing Gauge', 'Pattern Weights', 'Rotary Cutter',
                    'Cutting Mat', 'Ruler Set', 'Seam Guide', 'Tension Dial', 'Presser Foot Spring',
                    'Feed Dog Brush', 'Lint Brush', 'Needle Threader', 'Bobbin Set', 'Sewing Kit Travel',
                    'Machine Oil', 'Cleaning Brush Set', 'Sewing Feet Set', 'Extension Table', 'Foot Pedal',
                    'Power Cord', 'Stitch Selector', 'Thread Guide', 'Presser Bar Lifter', 'Needle Plate'
                ],
                'Knitting': [
                    'Knitting Needle Set', 'Yarn Assortment Premium', 'Bamboo Knitting Needles', 'Circular Needles Set',
                    'Stitch Markers Metal', 'Yarn Bowl Ceramic', 'Knitting Hooks Set', 'Crochet Hook Assortment',
                    'Yarn Weight Scale', 'Knitting Pattern Book', 'Tapestry Needle Set', 'Row Counter Device',
                    'Cable Knit Needles', 'Double Pointed Needles', 'Yarn Winder Machine', 'Blocking Mat Set',
                    'Needle Case Storage', 'Stitch Holder Set', 'Point Protectors', 'Needle Gauge',
                    'Tension Ring', 'Knit Bag Storage', 'Yarn Organizer', 'Pattern Reader', 'Lifeline Tool',
                    'Knot Puller', 'Weaving Needle', 'Blocking Pins', 'Blocking Wire', 'Yarn Cutter Pendant',
                    'Thumb Thing', 'Ring Stitch Marker', 'Progress Keeper', 'Pattern Holder', 'Yarn Labels',
                    'Notepads Knitting', 'Pencils Set', 'Eraser Tool', 'Sharpener', 'Sketchbook Knit'
                ],
                'Scrapbooking': [
                    'Scrapbook Paper Pack', 'Decorative Scissors Set', 'Glue Stick Set', 'Adhesive Tape Clear',
                    'Photo Corners Pack', 'Embellishment Stickers', 'Punch Set Decorative', 'Ink Pad Colors',
                    'Cardstock Bundle Premium', 'Stamp Set Clear', 'Washi Tape Assortment', 'Ribbon Collection',
                    'Brads and Eyelets', 'Corner Rounder', 'Paper Cutter Rotary', 'Scrapbook Album',
                    'Photo Slots', 'Journaling Stickers', 'Die Cutting Machine', 'Dies Set', 'Embossing Folder',
                    'Heat Gun', 'Embossing Powder', 'Marker Set Colors', 'Colored Pencils Set', 'Paint Pen Set',
                    'Blending Tools', 'Stamps Rubber Set', 'Letter Stamps', 'Number Stamps', 'Alphabet Stamps',
                    'Border Stamps', 'Texture Stamps', 'Inkpad Refill', 'Stamp Cleaner', 'Foam Adhesive Dots'
                ],
                'Craft Tools': [
                    'Craft Knife Set', 'Cutting Mat Professional', 'Metal Ruler', 'Pencil Sharpener',
                    'Eraser Collection', 'Glue Gun Hot', 'Hot Glue Sticks', 'Double Sided Tape',
                    'Craft Tweezers', 'Paper Punch', 'Hole Punch Professional', 'Stapler Heavy Duty',
                    'Craft Clamps Set', 'Magnifying Glass', 'Tool Organizer', 'Workbench Pad',
                    'Utility Knife', 'Cutting Guide', 'Circle Cutter', 'Paper Trimmer', 'Blade Refill Pack',
                    'Safety Mat', 'Storage Drawers', 'Hanging Organizer', 'Pegboard', 'Hooks Set',
                    'Labels Printable', 'Label Maker', 'Tape Labels', 'Storage Bins', 'Shelf Liners',
                    'Cork Board', 'Pin Set', 'Magnetic Strips', 'Fasteners Set', 'Clip Collection'
                ]
            },
            'Audible Books & Originals': {
                'Audiobooks': [
                    'Fiction Audiobook Collection', 'Mystery Thriller Audio', 'Romance Novel Audio', 'Science Fiction Audio',
                    'Fantasy Adventure Audio', 'Historical Fiction Audio', 'Crime Audiobook Series', 'Drama Series Audio',
                    'Self-Help Audiobook', 'Business Audiobook', 'Biography Audio', 'Memoir Audiobook',
                    'Young Adult Audio', 'Children Story Audio', 'Comedy Audio Collection', 'Horror Audiobook',
                    'Paranormal Romance Audio', 'Urban Fantasy Audio', 'Dystopian Audio', 'Suspense Audiobook',
                    'Literary Fiction Audio', 'Contemporary Romance Audio', 'Paranormal Mystery Audio', 'Cozy Mystery Audio',
                    'Romantic Suspense Audio', 'Historical Romance Audio', 'Dark Romance Audio', 'New Adult Audio',
                    'Coming of Age Audio', 'Family Saga Audio', 'Espionage Thriller Audio', 'Legal Thriller Audio',
                    'Medical Thriller Audio', 'Political Thriller Audio', 'Psychological Thriller Audio', 'Sci-Fi Thriller Audio',
                    'Time Travel Audio', 'Space Opera Audio', 'Cyberpunk Audio', 'Steampunk Audio'
                ],
                'Podcasts': [
                    'News Podcast Series', 'True Crime Podcast', 'Comedy Podcast', 'Business Podcast',
                    'Technology Podcast', 'Health Podcast Series', 'Sports Podcast', 'Entertainment Podcast',
                    'History Podcast', 'Science Podcast', 'Self-Development Podcast', 'Interview Series',
                    'Educational Podcast', 'Music Podcast', 'Travel Podcast', 'Food Podcast',
                    'Lifestyle Podcast', 'Fashion Podcast', 'Beauty Podcast', 'Finance Podcast',
                    'Investment Podcast', 'Career Podcast', 'Leadership Podcast', 'Motivation Podcast',
                    'Philosophy Podcast', 'Religion Podcast', 'Culture Podcast', 'Art Podcast',
                    'Literature Podcast', 'Writing Podcast', 'Parenting Podcast', 'Relationship Podcast'
                ],
                'Original Content': [
                    'Exclusive Audio Drama', 'Original Fiction Series', 'Documentary Audio', 'Comedy Special Audio',
                    'Performance Recording', 'Lecture Series', 'Workshop Recording', 'Panel Discussion',
                    'Author Reading', 'Storytelling Performance', 'Music Production', 'Creative Series',
                    'Scripted Drama', 'Audio Comedy Show', 'Narrative Experience', 'Immersive Story',
                    'Audio Play', 'Radio Drama', 'Experimental Audio', 'Avant Garde Audio',
                    'Ambient Audio', 'Sound Art', 'Sonic Journey', 'Audio Novel',
                    'Interactive Audio', 'Branching Audio Story', 'Audio Game', 'Audio Adventure'
                ],
                'Best Sellers': [
                    'Bestselling Fiction', 'Bestselling Non-Fiction', 'Chart Topper Audio', 'Popular Crime Series',
                    'Top Rated Romance', 'Acclaimed Fantasy', 'Award Winning Audio', 'Customer Favorite',
                    'Trending Audiobook', 'Most Listened', 'Highest Rated', 'Reader\'s Choice',
                    'Editor\'s Pick', 'Critically Acclaimed', 'Multi-Award Winner', 'Viral Hit Audio',
                    'Internet Sensation', 'Book Club Favorite', 'Literary Prize Winner', 'International Bestseller',
                    'Upcoming Bestseller', 'Rising Star Audio', 'Breakout Hit', 'Phenomena Audio'
                ],
                'New Releases': [
                    'Latest Release Audio', 'New Author Series', 'Fresh Content Audio', 'Recent Publication',
                    'Brand New Audiobook', 'Just Released Audio', 'Newest Addition', 'Latest Addition',
                    'New Series Launch', 'Recent Recording', 'Current Release', 'Hot New Audio',
                    'Upcoming Hit Audio', 'New Season Release', 'Latest Episode Series', 'New Season Drop',
                    'Fresh Release', 'Latest Drop', 'New Audio Edition', 'Updated Version Audio'
                ]
            },
            'Automotive': {
                'Car Electronics': [
                    'Car Stereo System Premium', 'Backup Camera HD', 'GPS Navigation Unit', 'Dash Cam 4K',
                    'Car Audio Amplifier', 'Speaker System Set', 'Bluetooth Car Kit', 'Apple CarPlay Head Unit',
                    'Android Auto Radio', 'Subwoofer System', 'Car Alarm System', 'Remote Car Starter',
                    'LED Car Lights', 'Power Window Motor', 'Car Security System', 'Parking Sensor Kit',
                    'Rearview Camera', 'Front Camera', 'Side Camera Set', ' 360 Camera System',
                    'Car Thermometer', 'Tire Pressure Monitor', 'Car Battery', 'Alternator', 'Starter Motor',
                    'Car Seat Warmer', 'Heated Steering Wheel', 'Window Defroster', 'Car Phone Charger',
                    'Car Power Inverter', 'Car USB Hub', 'Cigarette Lighter', 'Car Charger Multi Port'
                ],
                'Tools & Equipment': [
                    'Socket Wrench Set Complete', 'Torque Wrench Digital', 'Car Jack', 'Jack Stands Pair',
                    'Impact Driver', 'Battery Charger Smart', 'Multimeter Digital', 'Compression Tester',
                    'Oil Filter Wrench', 'Tire Pressure Gauge', 'Jumper Cables Heavy Duty', 'Spark Plug Socket Set',
                    'Brake Bleeding Kit', 'Engine Hoist', 'Car Lift', 'Air Compressor',
                    'Drill Bit Set', 'Hammer Set', 'Pliers Set', 'Screwdriver Set',
                    'Socket Organizer', 'Tool Box', 'Tool Cart', 'Work Light LED',
                    'Safety Glasses', 'Work Gloves', 'Safety Cones', 'Reflective Vest'
                ],
                'Car Care': [
                    'Car Wash Soap Premium', 'Tire Cleaner', 'Wax Polish Kit', 'Ceramic Coating',
                    'Glass Cleaner', 'Interior Detailing Spray', 'Brake Dust Cleaner', 'Oil Additive',
                    'Fuel System Cleaner', 'Coolant Flush', 'Transmission Fluid', 'Synthetic Oil Blend',
                    'Car Air Freshener', 'Odor Eliminator', 'Leather Cleaner', 'Carpet Shampoo',
                    'Floor Mat Cleaner', 'Upholstery Cleaner', 'Vinyl Protectant', 'Rubber Conditioner',
                    'Engine Degreaser', 'Wheel Cleaner', 'Polish Compound', 'Buffing Pad'
                ],
                'Interior Accessories': [
                    'Floor Mats Set Custom', 'Seat Covers Premium', 'Steering Wheel Cover', 'Sunshade Set',
                    'Cup Holder Insert', 'Car Organizer Multi', 'Trunk Storage Box', 'Backseat Organizer',
                    'Seat Protector', 'Dashboard Pad', 'Steering Lock', 'Anti-Slip Mat',
                    'Car Perfume', 'Phone Mount', 'Cigarette Lighter', 'Visor Organizer',
                    'Seat Cushion', 'Back Support', 'Lumbar Pillow', 'Neck Pillow', 'Armrest Pad'
                ],
                'Exterior Accessories': [
                    'Chrome Grille', 'Side Mirrors Replacement', 'Door Handles Custom', 'Bumper Guard',
                    'Roof Rack', 'Spoiler', 'Body Trim Set', 'Running Boards',
                    'Fender Flares', 'Window Visor', 'Mud Flaps', 'License Plate Frame',
                    'Car Emblem', 'Hood Protector', 'Door Guard', 'Rear Diffuser',
                    'Side Skirts', 'Front Lip', 'Splitter', 'Widebody Kit'
                ]
            },
            'Baby Products': {
                'Diapering': [
                    'Diaper Pack Size 1', 'Diaper Pack Size 2', 'Wipes Container', 'Diaper Cream',
                    'Diaper Pail', 'Changing Pad', 'Diaper Bag', 'Portable Changing Station',
                    'Diaper Dispenser', 'Washable Diaper', 'Training Pants', 'Swim Diapers',
                    'Diaper Rash Cream', 'Baby Oil', 'Wipe Warmer', 'Odor Control System',
                    'Diaper Holder', 'Changing Table Pad', 'Changing Table', 'Dresser Organizer'
                ],
                'Feeding': [
                    'Bottle Sterilizer', 'Bottle Set', 'High Chair', 'Feeding Tray',
                    'Baby Spoon Set', 'Baby Fork', 'Feeding Bibs', 'Food Container Set',
                    'Bottle Warmer', 'Bottle Brush Set', 'Milk Storage', 'Pumping Equipment',
                    'Teething Ring', 'Sippy Cups', 'Straw Cup', 'Breast Pump',
                    'Bottle Drying Rack', 'Bottle Organizer', 'Feeding Chair Booster', 'Placemat'
                ],
                'Baby Safety': [
                    'Crib Rail Guard', 'Safety Gates', 'Outlet Covers', 'Corner Guards',
                    'Door Lock', 'Cabinet Locks', 'Window Blind Cords', 'Bed Rails',
                    'Baby Monitor', 'Video Monitor', 'Motion Detector', 'Safety Lock Straps',
                    'Finger Pinch Guards', 'Bumpers', 'Sleep Positioner', 'Breathing Monitor',
                    'Temperature Monitor', 'Sound Sensor', 'Night Light', 'Humidifier'
                ],
                'Nursery': [
                    'Crib Set', 'Bassinet', 'Changing Table', 'Dresser',
                    'Closet Organizer', 'Storage Bins', 'Wall Decals', 'Night Light',
                    'Sound Machine', 'Humidifier', 'Thermometer', 'Rug',
                    'Curtains', 'Wall Mirror', 'Shelving Unit', 'Room Divider',
                    'Crib Mattress', 'Crib Sheets', 'Blanket', 'Pillow'
                ],
                'Baby Toys': [
                    'Rattle Set', 'Soft Blocks', 'Activity Mat', 'Gym Mobile',
                    'Teething Toys', 'Stacking Rings', 'Ball Set', 'Sensory Toy',
                    'Stuffed Animal', 'Crinkle Toy', 'Rattle Toys', 'Squeeze Toy',
                    'Baby Doll', 'Toy Keys', 'Hanging Toy', 'Bubble Maker',
                    'Spin Toy', 'Pop Toy', 'Shape Sorter', 'Building Blocks'
                ]
            },
            'CDs & Vinyl': {
                'Pop Music': [
                    'Pop Album Collection', 'Greatest Hits Pop', 'Pop Gold Collection', 'Pop Anthology',
                    'Modern Pop Hits', 'Classic Pop Vinyl', 'Pop Chart Toppers', 'Pop Icons',
                    'Pop Sensation Album', 'Pop Superstar CD', 'Pop Platinum Collection', 'Pop Legends',
                    'New Pop Release', 'Pop Remix Album', 'Pop Dance Mix', 'Pop Radio Hits',
                    'Pop Throwback', 'Pop Classics', 'Pop Best Of', 'Pop Essential'
                ],
                'Rock': [
                    'Rock Classics Album', 'Hard Rock Collection', 'Alternative Rock CD', 'Rock Legends',
                    'Classic Rock Vinyl', 'Modern Rock CD', 'Rock Anthology', 'Rock Gold Collection',
                    'Rock Classics Vinyl', 'Rock Icons', 'Rock Masters', 'Progressive Rock',
                    'Rock Hits Collection', 'Rock Greatest Hits', 'Indie Rock Album', 'Rock Essentials',
                    'Rock Power Ballads', 'Rock Stadium', 'Rock Punk', 'Rock Metal'
                ],
                'Classical': [
                    'Classical Symphony', 'Piano Concerto', 'Violin Master', 'Chamber Music',
                    'Orchestral Masterpiece', 'Classical Essentials', 'Great Composers', 'Classical Vinyl',
                    'Bach Collection', 'Beethoven Complete', 'Mozart Masterpieces', 'Classical Greats',
                    'Classical Gold', 'Symphony Collection', 'Classical Relaxation', 'Opera Collection',
                    'Ballet Music', 'Concerto Collection', 'Sonata Series', 'Chamber Ensemble'
                ],
                'Jazz': [
                    'Jazz Legends', 'Cool Jazz Album', 'Jazz Standards', 'Smooth Jazz Collection',
                    'Jazz Master Vinyl', 'Jazz Classics', 'Modern Jazz', 'Jazz Improvisation',
                    'Jazz Essentials', 'Jazz Icons', 'Bebop Collection', 'Jazz Gold',
                    'Free Jazz Album', 'Jazz Fusion', 'Jazz Trio', 'Jazz Piano',
                    'Jazz Saxophone', 'Jazz Drums', 'Jazz Bass', 'Jazz Vocal'
                ],
                'Vinyl Records': [
                    'Vinyl Album Pack', 'Limited Edition Vinyl', 'Reissue Vinyl', 'Collectors Vinyl',
                    'Audiophile Vinyl', 'Vintage Vinyl', 'Record Collection', 'Rare Vinyl',
                    'Album Artwork Vinyl', 'Gatefold Vinyl', 'Colored Vinyl', 'Special Edition Vinyl',
                    'First Edition Vinyl', 'Signed Vinyl', 'Picture Disc', 'Transparent Vinyl',
                    'Splatter Vinyl', 'Marble Vinyl', 'Glow in Dark', 'Ultimate Edition Vinyl'
                ]
            },
            'Everything Else': {
                'Misc Items': [
                    'Multi-Purpose Item', 'Useful Accessory', 'Handy Tool', 'Storage Solution',
                    'Organizational Item', 'Utility Product', 'Essential Item', 'General Purpose',
                    'Practical Tool', 'Everyday Product', 'Must Have Item', 'Convenience Product',
                    'Quality Good', 'Durable Product', 'Long Lasting Item', 'Value Product',
                    'Popular Choice', 'Customer Favorite', 'Best Seller', 'Trending Item'
                ],
                'Gift Cards': [
                    'Digital Gift Card $25', 'Digital Gift Card $50', 'Digital Gift Card $100', 'Store Credit',
                    'Shopping Voucher', 'Prepaid Card', 'E-Gift Card', 'Virtual Gift Card',
                    'Reloadable Gift Card', 'Birthday Card Option', 'Holiday Gift Card', 'Celebration Card',
                    'No Expiration Card', 'Digital Delivery', 'Instant Delivery', 'Custom Amount Card',
                    'Gift Card $10', 'Gift Card $20', 'Gift Card $75', 'Gift Card $150'
                ],
                'Currency': [
                    'International Currency', 'Exchange Rate Card', 'Travel Money', 'Currency Exchange',
                    'Forex Card', 'Multi-Currency Card', 'Travel Currency Kit', 'Money Exchanger',
                    'Currency Converter', 'International Transfer', 'Foreign Exchange', 'Currency Package',
                    'Travel Money Pack', 'Global Currency', 'Cross Border Payment', 'Currency Solution',
                    'Money Order', 'Bank Check', 'Wire Transfer', 'Digital Payment'
                ],
                'Collectibles': [
                    'Limited Edition Figure', 'Rare Collectible', 'Signed Memorabilia', 'Sports Card',
                    'Comic Book Collectible', 'Model Figurine', 'Collectible Statue', 'Vintage Item',
                    'Rare Edition', 'First Print Copy', 'Numbered Edition', 'Special Release',
                    'Exclusive Collectible', 'Autographed Item', 'Rare Treasure', 'Collector Piece',
                    'Premium Collectible', 'Ultra Rare Item', 'Graded Collectible', 'Certified Item'
                ],
                'Other': [
                    'Miscellaneous Product', 'Specialty Item', 'Unique Product', 'Special Purpose',
                    'Custom Item', 'Exclusive Offer', 'Limited Stock', 'Premium Selection',
                    'Featured Product', 'Best Value', 'Quality Selection', 'Choice Pick',
                    'Popular Item', 'Trending Product', 'Customer Favorite', 'Top Seller',
                    'New Addition', 'Latest Offering', 'Special Collection', 'Curated Selection'
                ]
            },
            'Grocery & Gourmet Food': {
                'Beverages': [
                    'Premium Coffee Beans', 'Tea Assortment', 'Organic Coffee', 'Espresso Blend',
                    'Decaf Coffee', 'Single Origin Coffee', 'Coffee Pod Set', 'Tea Collection',
                    'Green Tea Pack', 'Herbal Tea Mix', 'Iced Tea', 'Coffee Syrup',
                    'Flavored Coffee', 'Instant Coffee', 'Coffee Ground', 'Premium Tea',
                    'Matcha Tea', 'Chai Tea', 'Oolong Tea', 'White Tea'
                ],
                'Snacks': [
                    'Gourmet Snack Mix', 'Organic Chips', 'Granola Bars', 'Nut Mix Pack',
                    'Cheese Crisps', 'Protein Snack Bars', 'Trail Mix Assortment', 'Dried Fruit',
                    'Popcorn Collection', 'Pretzel Mix', 'Peanut Butter Packs', 'Energy Bars',
                    'Veggie Chips', 'Sesame Snack', 'Honey Snacks', 'Seed Mix',
                    'Dark Chocolate Nuts', 'Fruit Bars', 'Cereal Bars', 'Nut Butter Pack'
                ],
                'Breakfast Foods': [
                    'Organic Cereal', 'Granola Mix', 'Oatmeal Packets', 'Pancake Mix',
                    'Maple Syrup', 'Jam Collection', 'Honey Variety', 'Peanut Butter',
                    'Whole Wheat Bread', 'Bagel Pack', 'Muffin Mix', 'Waffle Mix',
                    'Breakfast Bar', 'Yogurt Starter', 'Smoothie Mix', 'Acai Pack',
                    'Cereal Flakes', 'Granola Clusters', 'Toast Mix', 'Pancake Syrup'
                ],
                'Canned Goods': [
                    'Organic Vegetables', 'Canned Fruit', 'Tomato Sauce', 'Canned Beans',
                    'Chickpea Can', 'Lentil Can', 'Black Beans', 'Kidney Beans',
                    'Corn Collection', 'Peas Pack', 'Mixed Vegetables', 'Mushroom Can',
                    'Olive Can', 'Artichoke Heart', 'Pumpkin Can', 'Soup Selection',
                    'Tuna Fish', 'Salmon Can', 'Sardines Can', 'Broth Can'
                ],
                'Organic': [
                    'Organic Coffee', 'Organic Tea', 'Organic Cereal', 'Organic Pasta',
                    'Organic Rice', 'Organic Flour', 'Organic Sugar', 'Organic Salt',
                    'Organic Honey', 'Organic Nuts', 'Organic Seeds', 'Organic Oil',
                    'Organic Spices', 'Organic Vinegar', 'Organic Sauce', 'Organic Snacks',
                    'Organic Chocolate', 'Organic Butter', 'Organic Milk', 'Organic Cheese'
                ]
            },
            'Health & Household': {
                'Vitamins': [
                    'Multivitamin Tablets', 'Vitamin C Tablets', 'Vitamin D Supplement', 'Omega 3 Capsule',
                    'Calcium Tablet', 'Iron Tablet', 'B Complex Vitamin', 'Vitamin A Supplement',
                    'Magnesium Tablet', 'Zinc Tablet', 'Potassium Tablet', 'Selenium Tablet',
                    'Vitamin E Capsule', 'Vitamin K2', 'Collagen Peptide', 'Biotin Tablet',
                    'Folic Acid', 'Niacin Tablet', 'Thiamine Tablet', 'Riboflavin Tablet'
                ],
                'Medical Supplies': [
                    'First Aid Kit', 'Bandage Assortment', 'Gauze Pads', 'Medical Tape',
                    'Thermometer Digital', 'Blood Pressure Cuff', 'Glucose Meter', 'Pulse Oximeter',
                    'Pain Relief Cream', 'Antibiotic Ointment', 'Muscle Rub', 'Hydrocolloid Patch',
                    'Elastic Bandage', 'Compression Sock', 'Heating Pad', 'Ice Pack',
                    'Wound Spray', 'Antiseptic Wipe', 'Medical Gloves', 'Syringe Set'
                ],
                'Household Supplies': [
                    'Cleaning Spray', 'Floor Cleaner', 'Disinfectant Wipes', 'Surface Cleaner',
                    'Glass Cleaner', 'Bathroom Cleaner', 'Toilet Cleaner', 'Drain Cleaner',
                    'Furniture Polish', 'Wood Cleaner', 'Carpet Cleaner', 'Laundry Detergent',
                    'Dish Soap', 'Hand Soap', 'Air Freshener', 'Trash Bag',
                    'Sponge Set', 'Cloth Towels', 'Mop Refill', 'Vacuum Bags'
                ],
                'Electronics': [
                    'Laptop Computer', 'Desktop Computer', 'Tablet Device', 'Smart Phone',
                    'Wireless Headphones', 'Bluetooth Speaker', 'Monitor Display', 'Keyboard',
                    'Computer Mouse', 'Webcam HD', 'USB Hub', 'Power Bank',
                    'Phone Charger', 'Laptop Charger', 'HDMI Cable', 'USB Cable',
                    'Screen Protector', 'Phone Case', 'Laptop Stand', 'Phone Stand',
                    'Smart Watch', 'Fitness Tracker', 'Camera Digital', 'Microphone USB',
                    'Audio Interface', 'Mechanical Keyboard', 'Gaming Mouse', 'Mousepad Large',
                    'Monitor Stand', 'Cable Organizer', 'USB Flash Drive', 'External Hard Drive',
                    'Router WiFi', 'Ethernet Cable', 'Smart Light', 'Smart Plug',
                    'Security Camera', 'Ring Doorbell', 'Smart Speaker', 'Portable Projector'
                ],
                'Sports Nutrition': [
                    'Protein Powder', 'Pre-Workout Mix', 'Post-Workout Shake', 'Amino Acid',
                    'Creatine Powder', 'Beta Alanine', 'Glutamine Powder', 'Branched Chain',
                    'Energy Drink', 'Electrolyte Drink', 'Weight Gainer', 'Meal Replacement',
                    'Recovery Shake', 'Hydration Drink', 'Endurance Bar', 'Muscle Builder',
                    'BCAA Powder', 'Whey Isolate', 'Casein Protein', 'Plant Protein'
                ]
            },
            'Apps & Games': {
                'Mobile Apps': [
                    'Productivity App', 'Photo Editing App', 'Social Media Manager', 'Note Taking App',
                    'Calendar Planner App', 'Password Manager', 'VPN App', 'Translation App',
                    'Weather App Premium', 'Fitness Tracker App', 'Meditation App', 'Language Learning App',
                    'Music Streaming App', 'Podcast App', 'Reading App', 'Dictionary App',
                    'Calculator Pro', 'Flashcard App', 'Habit Tracker', 'Sleep Tracking App',
                    'Nutrition Counter', 'Workout App', 'Yoga Classes App', 'Dance Lessons App',
                    'Drawing App', 'Photo Collage App', 'Video Editor App', 'Graphic Design App',
                    'Document Scanner', 'File Manager Pro', 'Backup App', 'Security App',
                    'Antivirus Mobile', 'Cleaner App', 'Battery Saver', 'Performance Booster'
                ],
                'Game Apps': [
                    'Action Game', 'Adventure Game', 'Puzzle Game', 'Strategy Game',
                    'RPG Game', 'Arcade Game', 'Sports Game', 'Racing Game',
                    'Simulation Game', 'Casual Game', 'Card Game', 'Board Game',
                    'Word Game', 'Trivia Game', 'Educational Game', 'Kids Game',
                    'Multiplayer Game', 'Shooter Game', 'Fighting Game', 'Platformer Game',
                    'Farming Game', 'City Building Game', 'Fantasy Game', 'Mystery Game',
                    'Survival Game', 'Horror Game', 'Adventure Puzzle', 'Role Playing Game',
                    'Tower Defense', 'Match 3 Game', 'Block Game', 'Endless Runner'
                ],
                'Utilities': [
                    'File Compression Tool', 'QR Code Scanner', 'Barcode Reader', 'Unit Converter',
                    'Currency Converter', 'Temperature Converter', 'Distance Calculator', 'Percentage Calculator',
                    'BMI Calculator', 'Age Calculator', 'Date Counter', 'World Clock',
                    'Alarm Clock', 'Timer App', 'Stopwatch App', 'Metronome App',
                    'Tuner App', 'Sound Meter', 'Decibel Meter', 'Light Meter',
                    'Compass App', 'GPS Tracker', 'Map App', 'Navigation App'
                ],
                'Desktop Software': [
                    'Office Suite', 'Spreadsheet Software', 'Presentation Tool', 'Database Manager',
                    'Photo Editor', 'Video Editor', 'Audio Recorder', 'Screen Recorder',
                    'Code Editor', 'IDE Software', 'Version Control', 'FTP Client',
                    'Email Client', 'Chat Software', 'VoIP Software', 'Video Conferencing',
                    'Project Manager', 'Time Tracker', 'Invoice Generator', 'Accounting Software',
                    'CRM Software', 'Email Marketing', 'Social Media Tool', 'Analytics Dashboard'
                ]
            },
            'Industrial & Scientific': {
                'Lab Equipment': [
                    'Microscope Digital', 'Microscope Slide Set', 'Test Tube Set', 'Beaker Set',
                    'Flask Set Glass', 'Burette Graduated', 'Pipette Set', 'Funnel Set',
                    'Mortar Pestle', 'Evaporating Dish', 'Watch Glass', 'Stirring Rod Set',
                    'Thermometer Laboratory', 'pH Meter Digital', 'Spectrophotometer', 'Centrifuge',
                    'Microscope Accessories', 'Lens Cleaner', 'Slide Storage', 'Sample Bottles',
                    'Laboratory Safety Kit', 'Goggles Safety', 'Gloves Nitrile', 'Lab Coat',
                    'First Aid Industrial', 'Fire Extinguisher', 'Emergency Shower', 'Eyewash Station'
                ],
                'Safety Equipment': [
                    'Hard Hat', 'Safety Helmet', 'Face Shield', 'Safety Goggles',
                    'Ear Protection', 'Respirator Mask', 'Work Gloves Leather', 'Cut Resistant Gloves',
                    'Steel Toe Boots', 'Slip Resistant Shoes', 'Safety Vest', 'Reflective Jacket',
                    'Fall Protection Harness', 'Safety Line Rope', 'Carabiner Clip', 'Landing Airbag',
                    'Traffic Cone', 'Warning Sign', 'Caution Tape', 'Barricade Tape',
                    'Strobe Light', 'Alarm Whistle', 'Emergency Horn', 'Communication Device'
                ],
                'Measurement Tools': [
                    'Digital Caliper', 'Micrometer', 'Tape Measure', 'Laser Measure',
                    'Digital Scale', 'Precision Scale', 'Angle Finder', 'Level Tool',
                    'Inclinometer', 'Pressure Gauge', 'Flow Meter', 'Humidity Meter',
                    'Moisture Meter', 'Lux Meter', 'Sound Level Meter', 'Vibration Meter',
                    'Thermocouple', 'IR Thermometer', 'Data Logger', 'Oscilloscope'
                ],
                'Power Tools Industrial': [
                    'Industrial Drill', 'Impact Drill', 'Rotary Hammer', 'Circular Saw',
                    'Band Saw', 'Jigsaw', 'Angle Grinder', 'Bench Grinder',
                    'Orbital Sander', 'Belt Sander', 'Planer Electric', 'Router Woodworking',
                    'Table Saw', 'Miter Saw', 'Nail Gun', 'Staple Gun',
                    'Chainsaw', 'Cut Off Tool', 'Concrete Breaker', 'Pneumatic Drill'
                ]
            },
            'Movies & TV': {
                'DVDs & Blu-ray': [
                    'Action Movie DVD', 'Comedy Movie DVD', 'Drama Movie DVD', 'Horror Movie DVD',
                    'Thriller Movie DVD', 'Romance Movie DVD', 'Sci-Fi Movie DVD', 'Fantasy Movie DVD',
                    'Adventure Movie DVD', 'Animation Movie DVD', 'Documentary DVD', 'Family Movie DVD',
                    'Action Blu-ray', 'Comedy Blu-ray', 'Drama Blu-ray', 'Horror Blu-ray',
                    'Thriller Blu-ray', 'Romance Blu-ray', 'Sci-Fi Blu-ray', 'Fantasy Blu-ray',
                    'Adventure Blu-ray', 'Animation Blu-ray', 'Documentary Blu-ray', 'Family Blu-ray',
                    'Box Set DVD', 'Collection Blu-ray', 'Movie Marathon Pack', 'Director\'s Cut'
                ],
                'TV Series': [
                    'Comedy Series Season', 'Drama Series Season', 'Crime Series Season', 'Thriller Series Season',
                    'Fantasy Series Season', 'Sci-Fi Series Season', 'Horror Series Season', 'Mystery Series Season',
                    'Adventure Series Season', 'Historical Series Season', 'Medical Series Season', 'Law Series Season',
                    'Complete Series Box', 'Collector Edition Series', 'Special Episode Pack', 'Retrospective Series'
                ],
                'Documentaries': [
                    'Nature Documentary', 'History Documentary', 'Science Documentary', 'Biography Documentary',
                    'Crime Documentary', 'Food Documentary', 'Travel Documentary', 'Music Documentary',
                    'Sports Documentary', 'Art Documentary', 'Technology Documentary', 'Environmental Documentary',
                    'Political Documentary', 'Medical Documentary', 'Adventure Documentary', 'Culture Documentary'
                ],
                'Streaming Content': [
                    'Streaming Service Gift Card', 'Movie Rental Gift Code', 'Premium Subscription', 'Family Plan',
                    'Annual Subscription', 'Premium Bundle', 'Content Pass', 'Early Access Pass',
                    'Ad-Free Upgrade', 'Download Pass', 'Offline Viewing', 'Multiple Device Pass'
                ]
            },
            'Musical Instruments': {
                'Guitars': [
                    'Acoustic Guitar Beginner', 'Acoustic Guitar Professional', 'Classical Guitar', 'Electric Guitar',
                    'Semi-Acoustic Guitar', 'Bass Guitar', 'Travel Guitar', 'Ukulele',
                    'Guitar Case Hard Shell', 'Guitar Case Soft', 'Guitar Strap', 'Guitar Stand',
                    'Guitar Tuner Digital', 'Guitar Capo', 'Guitar Strings Set', 'Guitar Picks Pack',
                    'Guitar Pedal', 'Guitar Amplifier', 'Guitar Cable', 'Guitar Polish'
                ],
                'Keyboards': [
                    'Piano 88 Keys', 'Keyboard 61 Keys', 'Keyboard 49 Keys', 'Synthesizer',
                    'Digital Piano Stage', 'MIDI Controller', 'Music Keyboard Stand', 'Piano Bench',
                    'Piano Lamp', 'Piano Pedal', 'Piano Key Light', 'Piano Sustain Pedal',
                    'Keyboard Case', 'Keyboard Bag', 'Keyboard Cable', 'Audio Interface'
                ],
                'Drums & Percussion': [
                    'Drum Set Acoustic', 'Drum Set Electronic', 'Drum Throne', 'Drum Sticks',
                    'Drum Pedal', 'Cymbal Set', 'Hi-Hat Stand', 'Cymbal Bag',
                    'Drum Microphone', 'Drum Mat', 'Tambourine', 'Maracas',
                    'Shaker Eggs', 'Cowbell', 'Triangle Bell', 'Xylophone'
                ],
                'Brass & Woodwind': [
                    'Trumpet', 'Trombone', 'French Horn', 'Tuba',
                    'Saxophone Soprano', 'Saxophone Alto', 'Saxophone Tenor', 'Saxophone Baritone',
                    'Clarinet', 'Flute', 'Oboe', 'Piccolo',
                    'Instrument Case', 'Mouthpiece Cleaner', 'Valve Oil', 'Reed Set'
                ],
                'String Instruments': [
                    'Violin Beginner', 'Violin Professional', 'Viola', 'Cello',
                    'Double Bass', 'Mandolin', 'Banjo', 'Lute',
                    'Violin Bow', 'Violin Strings', 'Chin Rest', 'Shoulder Rest',
                    'Rosin Cake', 'Tuner for Strings', 'Music Stand', 'String Cleaner'
                ]
            },
            'Office Products': {
                'Paper & Notebooks': [
                    'Notebook Blank A4', 'Notebook Lined', 'Notebook Grid', 'Notebook Dot',
                    'Spiral Notebook', 'Hardcover Notebook', 'Softcover Notebook', 'Premium Paper',
                    'Copy Paper Ream', 'Cardstock Pack', 'Construction Paper', 'Poster Board',
                    'Notebook Refill', 'Sticky Notes Pack', 'Adhesive Labels', 'Index Card Pack'
                ],
                'Writing Instruments': [
                    'Ballpoint Pens Pack', 'Gel Pens Set', 'Fountain Pen', 'Mechanical Pencil',
                    'Pencil Set', 'Markers Permanent', 'Highlighters Pack', 'Whiteboard Markers',
                    'Ink Cartridge', 'Pencil Lead Refill', 'Eraser Set', 'Pencil Sharpener Electric',
                    'Pen Holder', 'Desk Organizer', 'Writing Pad Leather', 'Desk Pad'
                ],
                'Office Supplies': [
                    'Stapler Heavy Duty', 'Staple Remover', 'Staples Box', 'Paper Clips Box',
                    'Binder Clips Set', 'Push Pins Box', 'Thumbtacks Box', 'Rubber Bands',
                    'Tape Dispenser', 'Scotch Tape', 'Masking Tape', 'Electrical Tape',
                    'File Folder', 'Manila Folder', 'Hanging File', 'File Cabinet'
                ],
                'Desk Furniture': [
                    'Office Desk', 'Computer Desk', 'Desk Organizer Set', 'Monitor Stand Riser',
                    'Office Chair', 'Desk Lamp LED', 'Desk Pad Mat', 'Keyboard Tray',
                    'Document Holder', 'File Organizer', 'Shelving Unit', 'Cabinet Storage'
                ]
            },
            'Patio, Lawn & Garden': {
                'Outdoor Furniture': [
                    'Patio Table Set', 'Dining Chair Outdoor', 'Lounge Chair', 'Bench Outdoor',
                    'Swing Chair Hanging', 'Rocking Chair', 'Garden Stool', 'End Table Outdoor',
                    'Coffee Table Outdoor', 'Console Table', 'Bar Table Height', 'Sectional Patio',
                    'Chaise Lounger', 'Daybed Outdoor', 'Hammock', 'Gazebo'
                ],
                'Garden Tools': [
                    'Shovel', 'Spade', 'Hoe Garden', 'Rake', 'Fork Garden',
                    'Trowel', 'Weeder Tool', 'Pruner Hand', 'Secateurs', 'Saw Garden',
                    'Hedge Trimmer', 'Leaf Blower', 'Trimmer String', 'Chainsaw Garden',
                    'Wheelbarrow', 'Garden Cart', 'Tool Rack', 'Tool Shed'
                ],
                'Lawn Care': [
                    'Lawn Mower Electric', 'Lawn Mower Gas', 'Riding Mower', 'Robot Mower',
                    'Grass Trimmer', 'Edger Lawn', 'Spreader Seed', 'Spreader Fertilizer',
                    'Aerator Lawn', 'Dethatcher', 'Grass Seed Bag', 'Fertilizer Bag',
                    'Weed Killer', 'Herbicide', 'Pesticide', 'Fungicide'
                ],
                'Landscaping': [
                    'Soil Bag', 'Mulch Bag', 'Compost Bag', 'Potting Soil',
                    'Landscape Fabric', 'Garden Border', 'Landscape Edging', 'Stepping Stone',
                    'Paver Brick', 'Gravel Bag', 'Sand Bag', 'Stone Landscape',
                    'Planter Box', 'Raised Bed', 'Garden Bed Kit', 'Trellis'
                ]
            },
            'Pet Supplies': {
                'Dog Products': [
                    'Dog Food Dry Premium', 'Dog Food Wet', 'Dog Treats Pack', 'Puppy Formula',
                    'Senior Dog Food', 'Dog Collar', 'Dog Leash', 'Dog Harness',
                    'Dog Bed', 'Dog Crate', 'Dog House', 'Dog Toys Plush',
                    'Dog Chew Toys', 'Dog Ball', 'Dog Rope Toy', 'Grooming Brush Dog',
                    'Dog Shampoo', 'Dog Nail Clipper', 'Dog Toothbrush', 'Dog Accessories'
                ],
                'Cat Products': [
                    'Cat Food Dry', 'Cat Food Wet', 'Cat Treats', 'Kitten Formula',
                    'Senior Cat Food', 'Cat Collar', 'Cat Leash Harness', 'Cat Bed',
                    'Cat Carrier', 'Cat House', 'Litter Box', 'Litter Deodorizer',
                    'Cat Litter', 'Cat Toys', 'Cat Climbing Tree', 'Cat Scratching Post',
                    'Cat Brush', 'Cat Shampoo', 'Cat Nail Clipper', 'Cat Accessories'
                ],
                'Small Pet Products': [
                    'Small Animal Food', 'Guinea Pig Food', 'Hamster Food', 'Rabbit Food',
                    'Bird Seed', 'Reptile Food', 'Pet Cage Small', 'Pet Bedding',
                    'Small Pet Toys', 'Water Bottle Pet', 'Food Bowl Pet', 'Pet Hideout',
                    'Pet Exercise Wheel', 'Pet Chew Toys', 'Pet Grooming Kit', 'Pet Accessories'
                ],
                'Pet Accessories': [
                    'Pet ID Tag', 'Pet Microchip', 'Pet Health Record', 'Pet Insurance',
                    'Pet Camera', 'Automatic Feeder', 'Water Fountain Pet', 'Pet Grooming Glove',
                    'Pet Lint Roller', 'Pet Waste Bags', 'Pet First Aid Kit', 'Pet Travel Carrier'
                ]
            },
            'Software': {
                'Antivirus & Security': [
                    'Antivirus Software Suite', 'Internet Security Suite', 'Total Security Suite', 'Parental Control',
                    'Password Manager', 'VPN Software', 'Firewall Software', 'Spyware Removal',
                    'Backup Software', 'Data Recovery Software', 'Encryption Software', 'Privacy Suite',
                    'Identity Theft Protection', 'Device Tracking', 'Remote Access', 'Network Monitor'
                ],
                'Productivity Software': [
                    'Office Suite', 'Word Processor', 'Spreadsheet Software', 'Presentation Software',
                    'Database Software', 'Project Manager', 'Time Tracker', 'Note Taking App',
                    'Calendar Software', 'Task Manager', 'Email Client', 'Contact Manager',
                    'Document Editor', 'PDF Reader', 'PDF Creator', 'Form Builder'
                ],
                'Creative Software': [
                    'Photo Editor Professional', 'Video Editor', 'Audio Editor', 'Graphic Design Suite',
                    'Illustration Software', 'Animation Software', 'CAD Software', '3D Modeling',
                    'Website Builder', 'CMS Software', '3D Rendering', 'Streaming Software',
                    'Screen Recorder', 'Virtual Studio', 'Color Grading', 'Special Effects'
                ],
                'Development Software': [
                    'IDE Software', 'Code Editor', 'Version Control', 'Database Manager',
                    'API Testing Tool', 'Debugging Tool', 'Performance Monitor', 'Memory Profiler',
                    'Build Automation', 'Container Platform', 'Testing Framework', 'Documentation Generator'
                ]
            },
            'Tools & Home Improvement': {
                'Hand Tools': [
                    'Hammer Claw', 'Hammer Ball Peen', 'Mallet', 'Axe', 'Hatchet',
                    'Saw Hand', 'Saw Circular', 'Saw Miter Box', 'Handsaw Set', 'Hacksaw',
                    'Wrench Set', 'Wrench Adjustable', 'Socket Set', 'Ratchet Set', 'Torque Wrench',
                    'Screwdriver Set', 'Screwdriver Phillips', 'Screwdriver Flathead', 'Screwdriver Multi',
                    'Pliers Set', 'Pliers Slip Joint', 'Pliers Needle Nose', 'Locking Pliers', 'Tongue Groove'
                ],
                'Power Tools': [
                    'Drill Cordless', 'Drill Impact', 'Rotary Hammer', 'Circular Saw',
                    'Jigsaw', 'Reciprocating Saw', 'Angle Grinder', 'Bench Grinder',
                    'Orbital Sander', 'Belt Sander', 'Detail Sander', 'Random Orbital Sander',
                    'Power Drill', 'Pressure Washer', 'Heat Gun', 'Multi-Tool'
                ],
                'Measuring Tools': [
                    'Tape Measure', 'Laser Measure', 'Digital Caliper', 'Micrometer',
                    'Level Spirit', 'Digital Level', 'Laser Level', 'Stud Finder',
                    'Moisture Meter', 'Voltage Tester', 'Multimeter', 'Thermal Camera'
                ],
                'Safety Equipment': [
                    'Safety Glasses', 'Safety Goggles', 'Face Shield', 'Dust Mask',
                    'Respirator N95', 'Ear Protection', 'Work Gloves', 'Cut Resistant Gloves',
                    'Steel Toe Boots', 'Tool Belt', 'Hard Hat', 'First Aid Kit'
                ]
            }
        }

        total_products = 0
        
        for cat_name, subcats_products in category_products.items():
            self.stdout.write(f'\n📂 Category: {cat_name}')
            
            category, _ = Category.objects.get_or_create(
                name=cat_name,
                defaults={'description': f'Browse our {cat_name.lower()} collection'}
            )
            
            products_created = 0
            
            for subcat_name, product_names in subcats_products.items():
                subcat, _ = Subcategory.objects.get_or_create(
                    category=category,
                    name=subcat_name
                )
                
                for i, product_name in enumerate(product_names):
                    unique_name = f'{product_name} #{i+1}'
                    
                    price = round(random.uniform(10.0, 999.0), 2)
                    stock = random.randint(25, 200)
                    
                    product, created = Product.objects.get_or_create(
                        name=unique_name,
                        defaults={
                            'category_ref': category,
                            'subcategory': subcat,
                            'price': price,
                            'stock': stock,
                            'description': f'{product_name} - Premium quality {subcat_name.lower()} from {cat_name}',
                            'short_description': f'{product_name} - ${price}'
                        }
                    )
                    
                    if created:
                        ProductSize.objects.get_or_create(
                            product=product,
                            size='M',
                            defaults={'quantity': stock}
                        )
                        products_created += 1
                        total_products += 1
            
            self.stdout.write(self.style.SUCCESS(f'  ✓ Added {products_created} products'))
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'✅ Complete! Total new products: {total_products}'))
        self.stdout.write(self.style.SUCCESS(f'  Total products in DB: {Product.objects.count()}'))
        self.stdout.write('='*60 + '\n')