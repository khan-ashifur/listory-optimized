#!/usr/bin/env python3
"""
Complete test script to verify Amazon listing generation and identify issues.
"""
import os
import sys
import django

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService

def test_listing_generation():
    """Test the complete listing generation process."""
    print("🧪 Testing Amazon listing generation...")
    
    # Create or get a test product
    from django.contrib.auth.models import User
    user, _ = User.objects.get_or_create(username='testuser', defaults={'email': 'test@example.com'})
    
    product, created = Product.objects.get_or_create(
        name='KZEN Electric Lunch Box Food Warmer',
        user=user,
        defaults={
            'description': 'Keep your meals warm with this portable electric lunch box. Perfect for office workers and travelers who need hot meals on the go.',
            'brand_name': 'KZEN',
            'brand_tone': 'professional',
            'target_platform': 'amazon',
            'price': 39.99,
            'categories': 'Kitchen & Dining, Small Appliances, Food Warmers',
            'features': 'Portable, Fast heating, Large capacity, Durable construction, Car-friendly',
            'target_keywords': 'electric lunch box, food warmer, portable heating',
            'seo_keywords': 'electric lunch box, portable food warmer, heated lunch container',
            'long_tail_keywords': 'electric lunch box for adults, portable food warmer for office, heated lunch container for car',
            'faqs': 'How long does it take to heat food? About 20-30 minutes. Can it be used in cars? Yes, it works with 12V car outlets.',
            'whats_in_box': 'Electric lunch box, power cord, car adapter, user manual, measuring cup',
            'competitor_urls': 'https://www.amazon.com/competitor1, https://www.amazon.com/competitor2'
        }
    )
    
    if created:
        print(f"✅ Created test product: {product.name}")
    else:
        print(f"♻️  Using existing product: {product.name}")
    
    # Initialize the listing generator
    generator = ListingGeneratorService()
    
    print("\n🚀 Generating Amazon listing...")
    try:
        listing = generator.generate_listing(product.id, 'amazon')
        
        print("\n📊 GENERATION RESULTS:")
        print("=" * 50)
        
        # Check title
        print(f"📝 Title: {listing.title[:100]}{'...' if len(listing.title) > 100 else ''}")
        
        # Check bullet points
        if listing.bullet_points:
            bullets_list = listing.bullet_points.split('\n\n') if listing.bullet_points else []
            print(f"🔸 Bullet Points: {len(bullets_list)} items")
            for i, bullet in enumerate(bullets_list[:3], 1):
                print(f"   {i}. {bullet[:80]}{'...' if len(bullet) > 80 else ''}")
        else:
            print("❌ Bullet Points: MISSING")
        
        # Check description
        if listing.long_description and len(listing.long_description.strip()) > 0:
            print(f"📄 Description: {len(listing.long_description)} chars")
            print(f"   Preview: {listing.long_description[:100]}{'...' if len(listing.long_description) > 100 else ''}")
        else:
            print("❌ Description: MISSING OR EMPTY")
        
        # Check keywords
        keywords_found = []
        if listing.keywords and len(listing.keywords.strip()) > 0: 
            keywords_found.append(f"General: {len(listing.keywords.split(','))}")
        if listing.amazon_backend_keywords and len(listing.amazon_backend_keywords.strip()) > 0: 
            keywords_found.append(f"Backend: {len(listing.amazon_backend_keywords.split(','))}")
        
        if keywords_found:
            print(f"🔑 Keywords: {', '.join(keywords_found)}")
        else:
            print("❌ Keywords: MISSING")
        
        # Check A+ content
        aplus_fields = []
        if listing.hero_title: aplus_fields.append("Hero title")
        if listing.hero_content: aplus_fields.append("Hero content")
        if listing.amazon_aplus_content: aplus_fields.append("A+ content")
        if listing.features: aplus_fields.append("Features")
        if listing.whats_in_box: aplus_fields.append("What's in box")
        if listing.trust_builders: aplus_fields.append("Trust builders")
        if listing.faqs: aplus_fields.append("FAQs")
        
        if aplus_fields:
            print(f"🎨 A+ Content: {', '.join(aplus_fields)}")
            if listing.amazon_aplus_content:
                print(f"   A+ Length: {len(listing.amazon_aplus_content)} chars")
        else:
            print("❌ A+ Content: MISSING")
        
        print("\n" + "=" * 50)
        return listing
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_listing_generation()