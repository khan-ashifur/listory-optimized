"""
Test Mixed Language A+ Content Generation
Instructions in English, Content in Target Language
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

def test_mixed_aplus():
    """Test the mixed language A+ content generation"""
    print("🌍 TESTING MIXED LANGUAGE A+ CONTENT")
    print("📋 Instructions: English | Content: Target Language")
    print("=" * 70)
    
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
        product.brand_tone = "professional"
        product.occasion = "none"
        product.save()
        
        print(f"📦 Product: {product.name}")
        print(f"🇩🇪 Market: Germany (de)")
        print(f"🎨 Brand Tone: professional")
        print(f"📝 Expected: Instructions in English, Content in German")
        
        print("\n🔄 Generating mixed language A+ content...")
        
        # Generate listing
        service.generate_listing(product.id, 'amazon')
        
        # Wait for generation
        print("⏳ Waiting for generation...")
        time.sleep(10)
        
        # Get the listing
        listing = GeneratedListing.objects.filter(
            product=product,
            platform='amazon'
        ).order_by('-created_at').first()
        
        if listing and listing.status == 'completed':
            print(f"✅ Generation successful!")
            
            # Analyze mixed language structure
            aplus_content = listing.amazon_aplus_content or ""
            print(f"\n📊 MIXED LANGUAGE A+ ANALYSIS:")
            print(f"  📏 Total Length: {len(aplus_content)} characters")
            
            # Check for mixed language patterns
            print(f"\n🔍 LANGUAGE DISTRIBUTION CHECK:")
            
            # Count English instruction words
            english_instructions = [
                "professional", "lifestyle", "image", "showing", "grid", 
                "features", "callout", "badges", "certifications", "visual"
            ]
            english_count = sum(aplus_content.lower().count(word) for word in english_instructions)
            
            # Count German content words  
            german_content = [
                "der", "die", "das", "und", "mit", "für", "qualität", 
                "produkt", "hochwertig", "zuverlässig"
            ]
            german_count = sum(aplus_content.lower().count(word) for word in german_content)
            
            print(f"    English instruction words: {english_count} occurrences")
            print(f"    German content words: {german_count} occurrences")
            
            # Check A+ sections
            print(f"\n📋 A+ SECTION ANALYSIS:")
            sections_found = {
                "Hero Section": "section1_hero" in aplus_content,
                "Features Section": "section2_features" in aplus_content,
                "Trust Section": "section3_trust" in aplus_content,
                "FAQ Section": "section4_faqs" in aplus_content
            }
            
            for section, found in sections_found.items():
                print(f"    {section}: {'✅' if found else '❌'}")
            
            # Check for image descriptions (should be in English)
            print(f"\n🖼️ IMAGE DESCRIPTION CHECK:")
            import re
            image_descriptions = re.findall(r'"imageDescription":\s*"([^"]+)"', aplus_content)
            
            if image_descriptions:
                for i, desc in enumerate(image_descriptions[:3]):
                    is_english = any(word in desc.lower() for word in english_instructions)
                    print(f"    Image {i+1}: {'✅ English' if is_english else '❌ Not English'}")
                    print(f"        {desc[:100]}...")
            else:
                print(f"    ❌ No image descriptions found")
            
            # Check actual content fields (should be in German)
            print(f"\n🇩🇪 CONTENT LANGUAGE CHECK:")
            
            content_fields = {
                "Hero Title": listing.hero_title,
                "Hero Content": listing.hero_content,
                "Features": listing.features,
                "Trust Builders": listing.trust_builders
            }
            
            for field_name, content in content_fields.items():
                if content:
                    has_german = any(word in content.lower() for word in german_content)
                    print(f"    {field_name}: {'✅ German' if has_german else '❌ Not German'}")
                    print(f"        Preview: {content[:80]}...")
                else:
                    print(f"    {field_name}: ❌ Empty")
            
            # Overall assessment
            print(f"\n🏆 MIXED LANGUAGE ASSESSMENT:")
            
            has_english_instructions = english_count >= 5
            has_german_content = german_count >= 3
            has_sections = sum(sections_found.values()) >= 3
            has_image_descriptions = len(image_descriptions) >= 2
            
            criteria_met = sum([
                has_english_instructions,
                has_german_content, 
                has_sections,
                has_image_descriptions
            ])
            
            print(f"    English Instructions: {'✅' if has_english_instructions else '❌'}")
            print(f"    German Content: {'✅' if has_german_content else '❌'}")
            print(f"    A+ Sections: {'✅' if has_sections else '❌'}")
            print(f"    Image Descriptions: {'✅' if has_image_descriptions else '❌'}")
            
            if criteria_met == 4:
                print(f"🎉 PERFECT: Mixed language A+ content structure!")
                score = "10/10"
            elif criteria_met >= 3:
                print(f"✅ GOOD: Mixed language structure mostly correct")
                score = "8/10"
            elif criteria_met >= 2:
                print(f"⚠️ PARTIAL: Some mixed language elements present")
                score = "6/10"
            else:
                print(f"❌ FAILED: Mixed language structure not implemented")
                score = "3/10"
            
            print(f"📊 Mixed Language Score: {score}")
            
        else:
            print(f"❌ Generation failed: {listing.status if listing else 'Not found'}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_mixed_aplus()