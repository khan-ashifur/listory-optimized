"""
Test Fixed A+ Content Generation for International Markets
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

def test_aplus_fixed():
    """Test the fixed A+ content generation"""
    print("🚀 TESTING FIXED A+ CONTENT FOR INTERNATIONAL MARKETS")
    print("="*70)
    
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
        
        print("\n🔄 Generating listing with FIXED A+ content system...")
        
        # Generate listing
        service.generate_listing(product.id, 'amazon')
        
        # Wait for generation
        print("⏳ Waiting for generation...")
        time.sleep(8)
        
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
            print(f"  📏 Length: {len(aplus_content)} characters")
            
            # Check for actual content (not just template)
            has_hero_title = listing.hero_title and listing.hero_title in aplus_content
            has_features = listing.features and any(feat in aplus_content for feat in listing.features.split('\n')[:3])
            has_trust = listing.trust_builders and any(trust in aplus_content for trust in listing.trust_builders.split('\n')[:3])
            
            print(f"\n🔍 DYNAMIC CONTENT CHECK:")
            print(f"  Hero title in HTML: {'✅' if has_hero_title else '❌'}")
            print(f"  Features in HTML: {'✅' if has_features else '❌'}")
            print(f"  Trust builders in HTML: {'✅' if has_trust else '❌'}")
            
            # Check for section modules
            sections_check = {
                "section1_hero": "section1_hero" in aplus_content,
                "section2_features": "section2_features" in aplus_content,
                "section3_trust": "section3_trust" in aplus_content,
                "section4_faqs": "section4_faqs" in aplus_content,
                "Hero Module": "hero" in aplus_content.lower(),
                "Features Module": "features" in aplus_content.lower(),
                "Trust Module": "trust" in aplus_content.lower(),
                "FAQ Module": "faq" in aplus_content.lower()
            }
            
            present_count = sum(1 for present in sections_check.values() if present)
            print(f"\n📋 SECTIONS DETECTED: {present_count}/{len(sections_check)}")
            for section, present in sections_check.items():
                print(f"    {section}: {'✅' if present else '❌'}")
            
            # Check for German market adaptation
            german_indicators = [
                "de" in aplus_content.lower(),
                product.brand_name in aplus_content,
                product.name in aplus_content
            ]
            
            adaptation_count = sum(german_indicators)
            print(f"\n🇩🇪 MARKET ADAPTATION: {adaptation_count}/3")
            
            # Final assessment
            print(f"\n🏆 FINAL ASSESSMENT:")
            
            is_dynamic = has_hero_title or has_features or has_trust
            is_comprehensive = len(aplus_content) > 5000
            has_sections = present_count >= 4
            
            if is_dynamic and is_comprehensive and has_sections:
                print("🎉 EXCELLENT: Full dynamic A+ content with all sections!")
                score = 10
            elif is_dynamic and (is_comprehensive or has_sections):
                print("✅ GOOD: Dynamic A+ content generated successfully!")
                score = 8
            elif is_dynamic:
                print("⚠️ PARTIAL: Some dynamic content but needs improvement")
                score = 6
            else:
                print("❌ FAILED: Still using static template")
                score = 3
            
            print(f"📊 A+ CONTENT SCORE: {score}/10")
            
            # Show sample of actual content
            if listing.hero_title:
                print(f"\n📝 ACTUAL HERO TITLE:")
                print(f"   {listing.hero_title}")
            
            if listing.features:
                features_preview = listing.features.split('\n')[:2]
                print(f"\n📝 ACTUAL FEATURES:")
                for feat in features_preview:
                    print(f"   • {feat}")
            
            # Show HTML preview
            if len(aplus_content) > 200:
                # Find the first actual content section
                import re
                content_match = re.search(r'<h3[^>]*>([^<]+)</h3>', aplus_content)
                if content_match:
                    print(f"\n📄 HTML CONTENT PREVIEW:")
                    print(f"   First heading: {content_match.group(1)}")
                
        else:
            print(f"❌ Generation failed: {listing.status if listing else 'Not found'}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_aplus_fixed()