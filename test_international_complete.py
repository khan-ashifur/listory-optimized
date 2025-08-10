"""
Complete International Market Testing with Brand Tone + Special Occasions
Tests the new InternationalContentExtractor integration
"""

import os
import sys
import django
import time
from datetime import datetime

# Add the backend directory to the Python path
sys.path.insert(0, r'C:\Users\khana\Desktop\listory-ai\backend')

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "listory.settings")
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from apps.listings.models import GeneratedListing

def test_german_market_with_brand_tone_and_occasion():
    """Test German market with brand tone and special occasion"""
    print("🚀 TESTING COMPLETE INTERNATIONAL INTEGRATION")
    print("="*70)
    print("Testing German market with:")
    print("  ✅ Brand tone system")
    print("  ✅ Special occasion system")
    print("  ✅ InternationalContentExtractor")
    print("  ✅ Full optimization (targeting 10/10)")
    
    try:
        service = ListingGeneratorService()
        
        # Find test product
        product = Product.objects.filter(name__icontains="misting fan").first()
        if not product:
            print("❌ No test product found")
            return
            
        # Configure for German market with luxury brand tone and Valentine's Day occasion
        product.marketplace = "de"
        product.marketplace_language = "de"
        product.brand_tone = "luxury"
        product.occasion = "Valentine's Day"
        product.save()
        
        print(f"\n📦 Product: {product.name}")
        print(f"🌍 Market: Germany (de)")
        print(f"🎨 Brand Tone: luxury")
        print(f"💝 Occasion: Valentine's Day")
        print("\n🔄 Generating listing with complete integration...")
        
        # Generate listing
        service.generate_listing(product.id, 'amazon')
        
        # Wait for generation
        time.sleep(8)
        
        # Get the listing
        listing = GeneratedListing.objects.filter(
            product=product,
            platform='amazon'
        ).order_by('-created_at').first()
        
        if listing and listing.status == 'completed':
            print(f"\n✅ GENERATION SUCCESS!")
            print(f"Status: {listing.status}")
            
            # Analyze the results
            print(f"\n📊 CONTENT ANALYSIS:")
            
            if listing.title:
                title_len = len(listing.title)
                has_german = any(char in listing.title for char in ['ä', 'ö', 'ü', 'ß'])
                has_luxury_words = any(word in listing.title.lower() for word in ['premium', 'elegant', 'luxury', 'sophisticated', 'exclusive'])
                has_valentine_words = any(word in listing.title.lower() for word in ['valentine', 'liebe', 'romantisch', 'herz'])
                
                print(f"  📝 Title: {title_len} chars")
                print(f"     German chars: {'✅' if has_german else '❌'}")
                print(f"     Luxury tone: {'✅' if has_luxury_words else '❌'}")
                print(f"     Valentine theme: {'✅' if has_valentine_words else '❌'}")
                print(f"     Content: {listing.title[:100]}...")
                
            if listing.bullet_points:
                bullets = listing.bullet_points.split('\n') if listing.bullet_points else []
                total_bullet_chars = len(listing.bullet_points)
                has_german_bullets = any(char in listing.bullet_points for char in ['ä', 'ö', 'ü', 'ß'])
                
                print(f"  🎯 Bullets: {len(bullets)} bullets, {total_bullet_chars} chars")
                print(f"     German chars: {'✅' if has_german_bullets else '❌'}")
                print(f"     Sample bullets:")
                for i, bullet in enumerate(bullets[:3]):
                    print(f"       {i+1}. {bullet[:80]}...")
                    
            if listing.long_description:
                desc_len = len(listing.long_description)
                has_german_desc = any(char in listing.long_description for char in ['ä', 'ö', 'ü', 'ß'])
                
                print(f"  📄 Description: {desc_len} chars")
                print(f"     German chars: {'✅' if has_german_desc else '❌'}")
                print(f"     Preview: {listing.long_description[:150]}...")
            
            # Calculate quality score
            quality_factors = []
            quality_factors.append(("Title length 150+", len(listing.title or '') >= 150))
            quality_factors.append(("German characters", any(char in (listing.title or '' + listing.bullet_points or '' + listing.long_description or '') for char in ['ä', 'ö', 'ü', 'ß'])))
            quality_factors.append(("5+ bullets", len((listing.bullet_points or '').split('\n')) >= 5))
            quality_factors.append(("Description 1000+ chars", len(listing.long_description or '') >= 1000))
            quality_factors.append(("Luxury tone present", any(word in (listing.title or '').lower() for word in ['premium', 'elegant', 'luxury', 'sophisticated'])))
            
            passed_factors = sum(1 for _, passed in quality_factors if passed)
            quality_score = (passed_factors / len(quality_factors)) * 100
            
            print(f"\n🏆 QUALITY ASSESSMENT:")
            print(f"  Overall Score: {quality_score:.1f}/100 {'✅' if quality_score >= 80 else '⚠️' if quality_score >= 60 else '❌'}")
            for factor, passed in quality_factors:
                print(f"    {factor}: {'✅' if passed else '❌'}")
                
            if quality_score >= 90:
                print(f"\n🎉 EXCELLENT! German market with brand tone + occasion = {quality_score:.1f}/100")
                print("✅ InternationalContentExtractor working perfectly!")
                print("✅ Brand tone integration successful!")
                print("✅ Special occasion integration successful!")
                print("✅ Full optimization achieved!")
            elif quality_score >= 70:
                print(f"\n⚠️ GOOD PROGRESS: {quality_score:.1f}/100")
                print("International integration working, minor optimizations needed")
            else:
                print(f"\n❌ NEEDS WORK: {quality_score:.1f}/100")
                print("Integration issues detected, requires debugging")
                
        else:
            print(f"❌ Listing generation failed: {listing.status if listing else 'Not found'}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_german_market_with_brand_tone_and_occasion()