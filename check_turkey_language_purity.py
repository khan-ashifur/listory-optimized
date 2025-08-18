"""
Check Turkey Language Purity - Verify Turkish content is pure
"""

import os
import sys
import django

# Django setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from django.contrib.auth.models import User

def check_language_purity():
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username='language_test')
    
    print("🔍 CHECKING TURKEY LANGUAGE PURITY")
    print("="*60)
    
    # Create product
    product = Product.objects.create(
        user=test_user,
        name="Sensei AI Translation Earbuds",
        description="AI-powered translation earbuds",
        brand_name="Sensei",
        brand_tone="premium",
        target_platform="amazon",
        marketplace="tr",
        marketplace_language="tr",
        categories="Electronics",
        features="144 languages, 60H battery, IPX7",
        target_audience="Turkish families"
    )
    
    try:
        listing = service.generate_listing(product_id=product.id, platform='amazon')
        
        if listing and listing.amazon_aplus_content:
            content = listing.amazon_aplus_content
            print(f"✅ A+ Content: {len(content)} chars")
            
            # Check for language contamination
            print(f"\n🔍 LANGUAGE CONTAMINATION CHECK:")
            
            # Spanish contamination (should be ZERO)
            spanish_phrases = [
                "Audífonos Traductores",
                "Garantizado para Familias en México",
                "familias mexicanas",
                "garantía nacional",
                "español",
                "México"
            ]
            
            spanish_found = []
            for phrase in spanish_phrases:
                if phrase in content:
                    spanish_found.append(phrase)
            
            if spanish_found:
                print(f"❌ SPANISH CONTAMINATION FOUND: {spanish_found}")
            else:
                print(f"✅ NO SPANISH CONTAMINATION")
            
            # English contamination check
            english_phrases = [
                "ENGLISH:",
                "premium quality, trusted brand",
                "innovative design, high performance",
                "customer testimonials, verified reviews"
            ]
            
            english_found = []
            for phrase in english_phrases:
                if phrase in content:
                    english_found.append(phrase)
            
            if english_found:
                print(f"❌ ENGLISH CONTAMINATION FOUND: {english_found}")
            else:
                print(f"✅ NO ENGLISH CONTAMINATION")
                
            # Turkish language verification
            turkish_phrases = [
                "Türk ailesi",
                "kaliteli",
                "güvenilir",
                "müşteri memnuniyeti",
                "yenilikçi tasarım",
                "günlük kullanım"
            ]
            
            turkish_found = []
            for phrase in turkish_phrases:
                if phrase in content:
                    turkish_found.append(phrase)
            
            print(f"\n✅ TURKISH CONTENT FOUND: {len(turkish_found)}/{len(turkish_phrases)} phrases")
            print(f"   Found: {turkish_found}")
            
            # Show first section for verification
            print(f"\n📄 FIRST A+ SECTION SAMPLE:")
            # Find first section content
            import re
            first_section = re.search(r'<div class="aplus-section.*?</div>', content, re.DOTALL)
            if first_section:
                section_text = first_section.group(0)[:500]
                print(section_text)
                print("...")
            
        else:
            print("❌ No A+ content generated")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        product.delete()

if __name__ == "__main__":
    check_language_purity()