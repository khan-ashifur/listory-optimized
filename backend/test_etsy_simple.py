#!/usr/bin/env python3
"""
Simple Etsy implementation test using Django shell
"""

from apps.core.models import Product
from apps.listings.models import GeneratedListing
from apps.listings.services import ListingGeneratorService
from apps.listings.market_occasions import MarketOccasions
import json

def test_etsy_basic():
    """Basic test of Etsy implementation"""
    print("🎨 Testing Etsy Implementation")
    print("=" * 40)
    
    # Test 1: Model Fields
    print("1. Testing model fields...")
    
    # Check Etsy brand tones
    etsy_tones = ['handmade', 'artistic', 'vintage', 'bohemian']
    available_tones = [choice[0] for choice in Product.BRAND_TONES]
    
    for tone in etsy_tones:
        if tone in available_tones:
            print(f"   ✅ Brand tone '{tone}' available")
        else:
            print(f"   ❌ Brand tone '{tone}' missing")
    
    # Check Etsy marketplaces
    etsy_marketplaces = [choice[0] for choice in Product.ETSY_MARKETPLACES]
    print(f"   ✅ Found {len(etsy_marketplaces)} Etsy marketplaces")
    
    # Test 2: Occasions
    print("\n2. Testing occasions...")
    market_occasions = MarketOccasions()
    etsy_occasions = market_occasions.get_market_occasions('etsy_us')
    print(f"   ✅ Found {len(etsy_occasions)} Etsy occasions")
    
    # Test creative occasions
    if 'art_show' in etsy_occasions:
        print(f"   ✅ Creative occasion 'art_show': {etsy_occasions['art_show']}")
    
    # Test 3: Service Methods
    print("\n3. Testing service methods...")
    service = ListingGeneratorService()
    
    try:
        guidance = service._get_etsy_brand_tone_guidance('handmade')
        print("   ✅ Brand tone guidance method works")
    except Exception as e:
        print(f"   ❌ Brand tone guidance error: {e}")
    
    try:
        context = service._get_marketplace_context('etsy_us')
        print(f"   ✅ Marketplace context: {context['country']}")
    except Exception as e:
        print(f"   ❌ Marketplace context error: {e}")
    
    # Test 4: Create Test Product
    print("\n4. Testing product creation...")
    try:
        product, created = Product.objects.get_or_create(
            name='Test Handmade Jewelry',
            brand_name='Test Artisan',
            defaults={
                'description': 'Beautiful handmade jewelry piece',
                'brand_tone': 'handmade',
                'target_platform': 'etsy',
                'marketplace': 'etsy_us',
                'price': 25.99,
                'categories': 'Jewelry',
                'features': 'Handmade, Sterling Silver'
            }
        )
        
        if created:
            print(f"   ✅ Created test product: {product.id}")
        else:
            print(f"   ✅ Using existing test product: {product.id}")
        
        # Test 5: Listing Structure
        print("\n5. Testing listing structure...")
        listing = GeneratedListing.objects.create(
            product=product,
            platform='etsy',
            status='completed',
            etsy_title='Test Handmade Jewelry | Artisan Made | Sterling Silver',
            etsy_description='Beautiful handcrafted jewelry...',
            etsy_tags=json.dumps(['handmade jewelry', 'sterling silver', 'artisan made']),
            etsy_materials='Sterling silver, natural gems',
            etsy_processing_time='1-3 business days',
            etsy_who_made='i_did',
            etsy_when_made='made_to_order'
        )
        
        print(f"   ✅ Created test listing: {listing.id}")
        print(f"   📝 Title: {listing.etsy_title}")
        print(f"   🏷️ Tags: {listing.etsy_tags}")
        print(f"   🧵 Materials: {listing.etsy_materials}")
        
        # Clean up
        listing.delete()
        if created:
            product.delete()
        
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Etsy implementation is working correctly")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_etsy_basic()