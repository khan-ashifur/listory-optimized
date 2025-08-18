"""
Quick Japan Test - Single Product Generation
"""

import os
import sys
import json
import django

# Django setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from django.contrib.auth.models import User

def quick_japan_test():
    print("\n🇯🇵 QUICK JAPAN TEST")
    print("=" * 40)
    
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username='quick_japan_test')
    
    # Create Japanese test product
    product = Product.objects.create(
        user=test_user,
        name="Premium Bluetooth Headphones",
        description="High-quality noise cancelling headphones",
        brand_name="TestBrand",
        brand_tone="professional",
        target_platform="amazon",
        marketplace="jp",
        marketplace_language="ja",  # Key fix!
        categories="Electronics/Audio",
        features="Noise Cancellation, 30hr Battery",
        target_audience="Professionals",
        occasion="kurisumasu"  # Christmas in Japanese
    )
    
    try:
        print("⏳ Generating Japanese listing...")
        listing = service.generate_listing(product_id=product.id, platform='amazon')
        
        if listing:
            title = listing.title or ''
            # Handle bullet points safely
            try:
                bullets = json.loads(listing.bullet_points) if listing.bullet_points else []
            except json.JSONDecodeError:
                bullets = listing.bullet_points.split('\n') if listing.bullet_points else []
            description = listing.long_description or ''
            
            print(f"\n📊 Generated Content:")
            print(f"Title ({len(title)} chars): {title}")
            print(f"\nFirst Bullet: {bullets[0] if bullets else 'None'}")
            print(f"\nDescription Preview ({len(description)} chars): {description[:200]}...")
            
            # Check for Japanese characters
            bullets_text = ' '.join(bullets) if isinstance(bullets, list) else str(bullets)
            full_text = f"{title} {bullets_text} {description}"
            has_hiragana = any('\u3040' <= char <= '\u309F' for char in full_text)
            has_katakana = any('\u30A0' <= char <= '\u30FF' for char in full_text)
            has_kanji = any('\u4E00' <= char <= '\u9FFF' for char in full_text)
            
            print(f"\n🇯🇵 Japanese Character Analysis:")
            print(f"  • Hiragana (ひらがな): {'✅ YES' if has_hiragana else '❌ NO'}")
            print(f"  • Katakana (カタカナ): {'✅ YES' if has_katakana else '❌ NO'}")
            print(f"  • Kanji (漢字): {'✅ YES' if has_kanji else '❌ NO'}")
            
            if has_hiragana or has_katakana or has_kanji:
                print(f"\n✅ SUCCESS: Japanese content generated!")
            else:
                print(f"\n❌ ISSUE: No Japanese characters found!")
                
            # Save sample
            with open('quick_japan_sample.json', 'w', encoding='utf-8') as f:
                json.dump({
                    'title': title,
                    'bullets': bullets if isinstance(bullets, list) else [bullets],
                    'description': description
                }, f, indent=2, ensure_ascii=False)
            
        else:
            print("❌ No listing generated")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        product.delete()

if __name__ == "__main__":
    quick_japan_test()