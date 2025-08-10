import os
import sys
import django

# Set up Django environment
sys.path.insert(0, 'backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.services import ListingGeneratorService
from apps.core.models import Product

print("Testing 10/10 Occasion Optimization System")
print("=" * 60)

# Test scenarios: Different occasions with different tones
test_scenarios = [
    {
        'name': 'Christmas + Professional Tone',
        'product_data': {
            'name': 'Wireless Bluetooth Headphones',
            'description': 'Premium noise-cancelling headphones with 30-hour battery life',
            'brand_name': 'AudioPro',
            'brand_tone': 'professional',
            'occasion': 'Christmas',
            'categories': 'Electronics, Audio',
            'features': 'Noise cancelling, 30-hour battery, Wireless, Premium sound quality',
            'price': 199.99,
        }
    },
    {
        'name': "Valentine's Day + Luxury Tone",
        'product_data': {
            'name': 'Silk Scarf Collection',
            'description': 'Hand-crafted silk scarves with artistic designs',
            'brand_name': 'LuxSilk',
            'brand_tone': 'luxury',
            'occasion': "Valentine's Day",
            'categories': 'Fashion, Accessories',
            'features': 'Pure silk, Hand-crafted, Artistic designs, Premium quality',
            'price': 299.99,
        }
    },
    {
        'name': "Mother's Day + Casual Tone",
        'product_data': {
            'name': 'Coffee Mug Set',
            'description': 'Beautiful ceramic coffee mugs with inspirational quotes',
            'brand_name': 'CozyHome',
            'brand_tone': 'casual',
            'occasion': "Mother's Day",
            'categories': 'Home, Kitchen',
            'features': 'Ceramic, Inspirational quotes, Microwave safe, Set of 4',
            'price': 39.99,
        }
    },
    {
        'name': 'Regular Listing (No Occasion) + Bold Tone',
        'product_data': {
            'name': 'Fitness Tracker Watch',
            'description': 'Advanced fitness tracking with heart rate monitoring',
            'brand_name': 'FitMax',
            'brand_tone': 'bold',
            'occasion': '',  # No occasion
            'categories': 'Electronics, Fitness',
            'features': 'Heart rate monitor, GPS, Water resistant, 7-day battery',
            'price': 149.99,
        }
    }
]

service = ListingGeneratorService()

if not service.client:
    print("❌ OpenAI client not initialized - check API key")
    exit()

for i, scenario in enumerate(test_scenarios, 1):
    print(f"\n{'='*20} Test {i}: {scenario['name']} {'='*20}")
    
    try:
        # Create test product
        product_data = scenario['product_data']
        product = Product.objects.create(**product_data)
        
        print(f"📋 Product: {product.name}")
        print(f"🎨 Brand Tone: {product.brand_tone}")
        print(f"🎉 Occasion: {product.occasion if product.occasion else 'None (Regular)'}")
        print(f"💰 Price: ${product.price}")
        
        # Generate listing
        print(f"🤖 Generating Amazon listing with GPT-5...")
        listing = service.generate_listing(product.id, 'amazon')
        
        # Display key results
        print(f"\n📝 Results:")
        print(f"Title (first 80 chars): {listing.title[:80]}...")
        
        # Check if occasion is prominent in title
        if product.occasion and product.occasion.lower() in listing.title.lower():
            print(f"✅ Occasion '{product.occasion}' found in title")
        elif product.occasion:
            print(f"❌ Occasion '{product.occasion}' NOT found in title")
        else:
            print(f"ℹ️ No occasion specified (regular listing)")
            
        # Check first bullet point
        bullets = listing.bullet_points.split('\n') if listing.bullet_points else []
        if bullets:
            first_bullet = bullets[0][:100]
            print(f"First bullet: {first_bullet}...")
            if product.occasion and product.occasion.lower() in first_bullet.lower():
                print(f"✅ Occasion '{product.occasion}' found in first bullet")
            elif product.occasion:
                print(f"❌ Occasion '{product.occasion}' NOT found in first bullet")
                
        # Check keyword integration
        if listing.keywords:
            keyword_text = listing.keywords.lower()
            if product.occasion and product.occasion.lower() in keyword_text:
                print(f"✅ Occasion keywords integrated")
            elif product.occasion:
                print(f"❌ Occasion keywords missing")
        
        # Check A+ content
        if listing.amazon_aplus_content:
            aplus_text = listing.amazon_aplus_content.lower()
            if product.occasion and product.occasion.lower() in aplus_text:
                print(f"✅ Occasion found in A+ content")
            elif product.occasion:
                print(f"❌ Occasion missing from A+ content")
        
        print(f"🔢 Total listing length: {len(listing.long_description)} chars")
        
        # Clean up
        product.delete()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if 'product' in locals():
            product.delete()

print(f"\n{'='*60}")
print("🎯 Occasion Optimization Test Complete!")
print("Key success criteria:")
print("✅ Occasion in title when specified")
print("✅ First bullet mentions occasion benefit") 
print("✅ Keywords prioritize occasion terms")
print("✅ A+ content uses occasion theme")
print("✅ Regular listings work without occasion")