"""
Check Turkey A+ Content Localization - Labels in Turkish, Image Descriptions in English
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

def check_turkey_aplus():
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username='turkey_aplus_check')
    
    print("🇹🇷 CHECKING TURKEY A+ CONTENT LOCALIZATION")
    print("="*60)
    print("✅ Expected: Labels in Turkish (Anahtar Kelimeler, Görsel Strateji, SEO Odak)")
    print("✅ Expected: Image descriptions in English")
    print("="*60)
    
    # Create product for Turkey market
    product = Product.objects.create(
        user=test_user,
        name="Premium Wireless Bluetooth Headphones",
        description="High-quality wireless headphones with active noise cancellation",
        brand_name="SoundMaster",
        brand_tone="premium",
        target_platform="amazon",
        marketplace="tr",
        marketplace_language="tr",
        categories="Electronics/Audio/Headphones",
        features="Active Noise Cancellation, 40H Battery, Wireless",
        target_audience="Turkish professionals",
        occasion="kurban_bayrami"
    )
    
    try:
        print("🔄 Generating Turkey listing...")
        listing = service.generate_listing(product_id=product.id, platform='amazon')
        
        if listing and listing.amazon_aplus_content:
            aplus_content = listing.amazon_aplus_content
            print(f"📄 A+ Content Generated: {len(aplus_content)} characters")
            
            # Check for Turkish labels
            turkish_labels = ['Anahtar Kelimeler', 'Görsel Strateji', 'SEO Odak']
            turkish_found = []
            for label in turkish_labels:
                if label in aplus_content:
                    turkish_found.append(label)
            
            print(f"\n🇹🇷 TURKISH LABELS CHECK:")
            print(f"   Found: {len(turkish_found)}/3 Turkish labels")
            for label in turkish_found:
                print(f"   ✅ {label}")
            
            # Check for English image descriptions
            english_image_patterns = [
                'Turkish family lifestyle image',
                'showing product in use',
                '(970x600px)',
                'Professional product shots',
                'Feature callouts with'
            ]
            
            english_image_found = []
            for pattern in english_image_patterns:
                if pattern.lower() in aplus_content.lower():
                    english_image_found.append(pattern)
            
            print(f"\n🇺🇸 ENGLISH IMAGE DESCRIPTIONS CHECK:")
            print(f"   Found: {len(english_image_found)} English image patterns")
            for pattern in english_image_found:
                print(f"   ✅ {pattern}")
            
            # Look for any Turkish image descriptions that shouldn't be there
            turkish_image_words = ['görsel', 'resim', 'fotoğraf', 'gösterimi']
            turkish_image_found = []
            for word in turkish_image_words:
                if word in aplus_content.lower():
                    turkish_image_found.append(word)
            
            if turkish_image_found:
                print(f"\n⚠️ POTENTIAL TURKISH IMAGE DESCRIPTIONS:")
                for word in turkish_image_found:
                    print(f"   🔍 Found: {word}")
            else:
                print(f"\n✅ NO TURKISH IMAGE DESCRIPTIONS FOUND (Good!)")
            
            # Overall assessment
            print(f"\n🏆 OVERALL LOCALIZATION ASSESSMENT:")
            if len(turkish_found) == 3 and len(english_image_found) > 0:
                print("🎉 PERFECT! Turkish labels + English image descriptions")
                print("✅ Localization requirements met")
            elif len(turkish_found) == 3:
                print("✅ Turkish labels correct")
                print("🔍 Need to verify English image descriptions")
            else:
                print("⚠️ Turkish labels incomplete")
                print(f"   Missing: {3 - len(turkish_found)} labels")
                
        else:
            print("❌ No A+ content generated")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    finally:
        product.delete()

if __name__ == "__main__":
    check_turkey_aplus()