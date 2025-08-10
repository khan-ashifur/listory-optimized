"""
Simple A+ Content Test for German Market
Quick test to verify A+ content enhancement is working
"""

import os
import sys
import django
import time

# Add the backend directory to the Python path
sys.path.insert(0, r'C:\Users\khana\Desktop\listory-ai\backend')

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "listory.settings")
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from apps.listings.models import GeneratedListing

def test_simple_aplus():
    """Simple test of A+ content for German market"""
    print("🚀 SIMPLE A+ CONTENT TEST - GERMAN MARKET")
    print("="*60)
    
    try:
        service = ListingGeneratorService()
        
        # Find test product
        product = Product.objects.filter(name__icontains="misting fan").first()
        if not product:
            print("❌ No test product found")
            return
        
        # Configure for German market
        product.marketplace = "de"
        product.marketplace_language = "de"
        product.brand_tone = "luxury"
        product.occasion = "Valentine's Day"
        product.save()
        
        print(f"📦 Product: {product.name}")
        print(f"🌍 Market: Germany (de)")
        print(f"🎨 Brand Tone: luxury")
        print(f"💝 Occasion: Valentine's Day")
        
        print("\n🔄 Generating listing with A+ content enhancement...")
        
        # Generate listing
        service.generate_listing(product.id, 'amazon')
        
        # Wait for generation
        print("⏳ Waiting for generation...")
        time.sleep(6)
        
        # Get the listing
        listing = GeneratedListing.objects.filter(
            product=product,
            platform='amazon'
        ).order_by('-created_at').first()
        
        if listing and listing.status == 'completed':
            print(f"✅ Generation successful!")
            
            # Check A+ content
            aplus_content = listing.amazon_aplus_content or ""
            print(f"\n📊 A+ CONTENT ANALYSIS:")
            print(f"  Length: {len(aplus_content)} characters")
            
            if len(aplus_content) > 1000:
                print("  ✅ A+ content generated (substantial)")
                
                # Look for key indicators
                has_hero = "hero" in aplus_content.lower()
                has_features = "features" in aplus_content.lower()
                has_strategy = "strategy" in aplus_content.lower()
                has_visual = "visual" in aplus_content.lower() or "template" in aplus_content.lower()
                
                print(f"  Hero section: {'✅' if has_hero else '❌'}")
                print(f"  Features: {'✅' if has_features else '❌'}")
                print(f"  Strategy: {'✅' if has_strategy else '❌'}")
                print(f"  Visual elements: {'✅' if has_visual else '❌'}")
                
                # Show first 200 characters
                print(f"\n📄 A+ CONTENT PREVIEW:")
                print(f"   {aplus_content[:200]}...")
                
                # Count sections
                sections = sum([has_hero, has_features, has_strategy, has_visual])
                print(f"\n🏆 A+ CONTENT SCORE: {sections}/4 sections present")
                
                if sections >= 3:
                    print("✅ SUCCESS: A+ content enhancement working!")
                else:
                    print("⚠️ Partial success, needs improvement")
                    
            elif len(aplus_content) > 0:
                print("  ⚠️ A+ content generated but minimal")
                print(f"     Content: {aplus_content}")
            else:
                print("  ❌ No A+ content generated")
                
        else:
            print(f"❌ Generation failed: {listing.status if listing else 'Not found'}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple_aplus()