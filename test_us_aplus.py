"""
Test US Market A+ Content Generation Structure
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

def test_us_aplus():
    """Test US A+ content generation to understand the structure"""
    print("🇺🇸 TESTING US MARKET A+ CONTENT STRUCTURE")
    print("=" * 60)
    
    try:
        service = ListingGeneratorService()
        
        # Find test product
        product = Product.objects.filter(name__icontains="misting fan").first()
        if not product:
            print("❌ No test product found")
            return
        
        # Configure for US market (default)
        product.marketplace = "us"
        product.marketplace_language = "en"
        product.brand_tone = "luxury"
        product.occasion = "Valentine's Day"
        product.save()
        
        print(f"📦 Product: {product.name}")
        print(f"🇺🇸 Market: USA (default)")
        print(f"🎨 Brand Tone: luxury")
        print(f"💝 Occasion: Valentine's Day")
        
        print("\n🔄 Generating US A+ content...")
        
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
            print(f"✅ US Generation successful!")
            
            # Analyze US A+ structure
            aplus_content = listing.amazon_aplus_content or ""
            print(f"\n📊 US A+ CONTENT STRUCTURE ANALYSIS:")
            print(f"  📏 Length: {len(aplus_content)} characters")
            
            # Check A+ field population
            print(f"\n🔍 US A+ CONTENT FIELDS:")
            print(f"  hero_title: '{listing.hero_title[:100] if listing.hero_title else 'None'}'")
            print(f"  hero_content: '{listing.hero_content[:150] if listing.hero_content else 'None'}'...")
            print(f"  features: {len(listing.features.split('\\n')) if listing.features else 0} items")
            print(f"  trust_builders: {len(listing.trust_builders.split('\\n')) if listing.trust_builders else 0} items")
            print(f"  faqs: {len(listing.faqs.split('\\n\\n')) if listing.faqs else 0} items")
            
            # Check HTML structure patterns
            import re
            print(f"\n🏗️ US HTML STRUCTURE ANALYSIS:")
            
            # Find section modules
            sections = {
                "Hero Modules": len(re.findall(r'section1_hero|hero-module', aplus_content)),
                "Feature Modules": len(re.findall(r'section2_features|features-module', aplus_content)),
                "Trust Modules": len(re.findall(r'section3_trust|trust-module', aplus_content)),
                "FAQ Modules": len(re.findall(r'section4_faqs|faq-module', aplus_content)),
                "Comparison Modules": len(re.findall(r'section5_comparison|comparison-module', aplus_content))
            }
            
            for section, count in sections.items():
                print(f"    {section}: {count} found")
            
            # Extract key HTML patterns
            print(f"\n📋 US A+ HTML PATTERNS:")
            
            # Check for aplus-module classes
            aplus_modules = re.findall(r'<div class="aplus-module[^"]*"', aplus_content)
            print(f"    aplus-module divs: {len(aplus_modules)}")
            
            # Check for section classes
            section_cards = re.findall(r'<div class="aplus-section-card[^"]*"', aplus_content)
            print(f"    aplus-section-card divs: {len(section_cards)}")
            
            # Check for responsive classes
            responsive_classes = ["sm:px-4", "sm:text-2xl", "sm:p-6"]
            responsive_count = sum(aplus_content.count(cls) for cls in responsive_classes)
            print(f"    responsive classes: {responsive_count} found")
            
            # Extract first few section headings
            headings = re.findall(r'<h3[^>]*>([^<]+)</h3>', aplus_content)
            print(f"\n📝 US A+ SECTION HEADINGS:")
            for i, heading in enumerate(headings[:5]):
                print(f"    {i+1}. {heading}")
            
            # Show HTML structure sample
            if len(aplus_content) > 500:
                print(f"\n📄 US A+ HTML STRUCTURE SAMPLE:")
                # Get first module structure
                first_module = aplus_content[:800]
                lines = first_module.split('\n')[:10]
                for line in lines:
                    if line.strip():
                        print(f"    {line.strip()}")
            
            # Final US assessment
            print(f"\n🏆 US A+ ASSESSMENT:")
            has_dynamic = listing.hero_title and listing.features
            has_length = len(aplus_content) > 5000
            has_modules = len(aplus_modules) >= 3
            
            print(f"    Dynamic content: {'✅' if has_dynamic else '❌'}")
            print(f"    Comprehensive length: {'✅' if has_length else '❌'}")
            print(f"    Multiple modules: {'✅' if has_modules else '❌'}")
            
            score = sum([has_dynamic, has_length, has_modules])
            print(f"    US A+ Quality: {score}/3 ({'Perfect' if score == 3 else 'Good' if score == 2 else 'Needs Work'})")
            
        else:
            print(f"❌ US Generation failed: {listing.status if listing else 'Not found'}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_us_aplus()