"""
Test A+ Content International Market Optimization
Verify that international markets get full A+ content like US market
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

def test_aplus_content_international():
    """Test A+ content quality for German market vs US market"""
    print("🚀 TESTING A+ CONTENT INTERNATIONAL OPTIMIZATION")
    print("="*70)
    print("Comparing German market A+ content quality with US market")
    
    try:
        service = ListingGeneratorService()
        
        # Find test product
        product = Product.objects.filter(name__icontains="misting fan").first()
        if not product:
            print("❌ No test product found")
            return
        
        # Test German market first
        print(f"\n🇩🇪 TESTING GERMAN MARKET A+ CONTENT")
        print("-" * 50)
        
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
        print("\n🔄 Generating German listing...")
        
        # Generate listing
        service.generate_listing(product.id, 'amazon')
        
        # Wait for generation
        time.sleep(8)
        
        # Get the German listing
        german_listing = GeneratedListing.objects.filter(
            product=product,
            platform='amazon'
        ).order_by('-created_at').first()
        
        if german_listing and german_listing.status == 'completed':
            print(f"✅ German generation success!")
            
            # Analyze A+ content
            aplus_content = german_listing.amazon_aplus_content or ""
            
            print(f"\n📊 GERMAN A+ CONTENT ANALYSIS:")
            print(f"  📏 Total length: {len(aplus_content)} chars")
            
            # Check for key A+ sections
            sections = {
                "Hero Section": "hero" in aplus_content.lower(),
                "Features Section": "features" in aplus_content.lower(),
                "Trust Builders": "trust" in aplus_content.lower(),
                "FAQs": "faq" in aplus_content.lower(),
                "PPC Strategy": "ppc" in aplus_content.lower(),
                "Visual Templates": "visual" in aplus_content.lower() or "template" in aplus_content.lower(),
                "Overall Strategy": "strategy" in aplus_content.lower()
            }
            
            present_sections = sum(1 for present in sections.values() if present)
            print(f"  📋 Sections present: {present_sections}/{len(sections)}")
            
            for section, present in sections.items():
                print(f"    {section}: {'✅' if present else '❌'}")
            
            # Check for German market cultural adaptation
            german_indicators = [
                "germany" in aplus_content.lower(),
                "german" in aplus_content.lower(),
                "deutschland" in aplus_content.lower(),
                "european" in aplus_content.lower(),
                "eu market" in aplus_content.lower()
            ]
            
            german_adaptation = sum(1 for indicator in german_indicators if indicator)
            print(f"  🇩🇪 German market adaptation: {german_adaptation}/5")
            
            # Show sample A+ content
            if len(aplus_content) > 200:
                print(f"\n📄 SAMPLE A+ CONTENT:")
                print(f"   {aplus_content[:300]}...")
            else:
                print(f"\n⚠️ A+ content too short: {aplus_content}")
                
        else:
            print(f"❌ German listing generation failed")
            return
        
        # Now test US market for comparison
        print(f"\n\n🇺🇸 TESTING US MARKET A+ CONTENT (for comparison)")
        print("-" * 50)
        
        # Configure for US market
        product.marketplace = "com"
        product.marketplace_language = "en"
        product.brand_tone = "luxury"
        product.occasion = "Valentine's Day"
        product.save()
        
        print(f"📦 Product: {product.name}")
        print(f"🌍 Market: USA (com)")
        print(f"🎨 Brand Tone: luxury")
        print(f"💝 Occasion: Valentine's Day")
        print("\n🔄 Generating US listing...")
        
        # Generate listing
        service.generate_listing(product.id, 'amazon')
        
        # Wait for generation
        time.sleep(8)
        
        # Get the US listing
        us_listing = GeneratedListing.objects.filter(
            product=product,
            platform='amazon'
        ).order_by('-created_at').first()
        
        if us_listing and us_listing.status == 'completed':
            print(f"✅ US generation success!")
            
            # Analyze A+ content
            us_aplus_content = us_listing.amazon_aplus_content or ""
            
            print(f"\n📊 US A+ CONTENT ANALYSIS:")
            print(f"  📏 Total length: {len(us_aplus_content)} chars")
            
            # Check for key A+ sections
            us_sections = {
                "Hero Section": "hero" in us_aplus_content.lower(),
                "Features Section": "features" in us_aplus_content.lower(),
                "Trust Builders": "trust" in us_aplus_content.lower(),
                "FAQs": "faq" in us_aplus_content.lower(),
                "PPC Strategy": "ppc" in us_aplus_content.lower(),
                "Visual Templates": "visual" in us_aplus_content.lower() or "template" in us_aplus_content.lower(),
                "Overall Strategy": "strategy" in us_aplus_content.lower()
            }
            
            us_present_sections = sum(1 for present in us_sections.values() if present)
            print(f"  📋 Sections present: {us_present_sections}/{len(us_sections)}")
            
            # Compare German vs US A+ content
            print(f"\n🏆 COMPARISON RESULTS:")
            print(f"  German A+ content: {len(aplus_content)} chars, {present_sections}/{len(sections)} sections")
            print(f"  US A+ content: {len(us_aplus_content)} chars, {us_present_sections}/{len(us_sections)} sections")
            
            if len(aplus_content) >= len(us_aplus_content) * 0.8 and present_sections >= us_present_sections * 0.8:
                print(f"  ✅ German A+ content quality matches US standard!")
                quality_score = 10
            elif len(aplus_content) >= len(us_aplus_content) * 0.6 and present_sections >= us_present_sections * 0.6:
                print(f"  ⚠️ German A+ content good but needs improvement")
                quality_score = 7
            else:
                print(f"  ❌ German A+ content significantly behind US standard")
                quality_score = 4
                
            print(f"\n🎯 FINAL A+ CONTENT SCORE: {quality_score}/10")
            
            if quality_score >= 8:
                print("🎉 SUCCESS: International A+ content optimization working!")
            else:
                print("⚠️ NEEDS IMPROVEMENT: International A+ content requires enhancement")
                
        else:
            print(f"❌ US listing generation failed")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_aplus_content_international()