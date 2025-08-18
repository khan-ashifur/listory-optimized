"""
Quick UAE Test - Single Product Generation with Eid
Tests UAE market with Arabic language and cultural nuances
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

def quick_uae_test():
    print("\n🇦🇪 QUICK UAE TEST - ARABIC CONTENT GENERATION")
    print("=" * 50)
    
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username='quick_uae_test')
    
    # Create UAE test product with Eid occasion
    product = Product.objects.create(
        user=test_user,
        name="Premium Smart Air Purifier",
        description="Advanced HEPA air purifier with smart controls for clean indoor air",
        brand_name="PureAir",
        brand_tone="luxurious",
        target_platform="amazon",
        marketplace="ae",
        marketplace_language="ar",  # Arabic language - CRITICAL!
        categories="Home/Health/Air Quality",
        features="HEPA Filter, Smart Controls, WiFi Enabled, App Control",
        target_audience="UAE families and health-conscious individuals",
        occasion="eid_al_fitr"  # Eid al-Fitr occasion
    )
    
    try:
        print("⏳ Generating Arabic listing for UAE market...")
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
            
            # Check for Arabic characters (Arabic Unicode range)
            bullets_text = ' '.join(bullets) if isinstance(bullets, list) else str(bullets)
            full_text = f"{title} {bullets_text} {description}"
            has_arabic = any('\u0600' <= char <= '\u06FF' for char in full_text)
            
            # Check for specific Arabic words indicating quality
            arabic_quality_indicators = ['الأفضل', 'ممتاز', 'فاخر', 'جودة', 'موثوق', 'عيد', 'مبارك']
            has_quality_words = any(word in full_text for word in arabic_quality_indicators)
            
            # Check for Eid-related content
            eid_keywords = ['عيد', 'الفطر', 'مبارك', 'هدية', 'العائلة', 'للأهل']
            has_eid_content = any(word in full_text for word in eid_keywords)
            
            print(f"\n🇦🇪 Arabic Content Analysis:")
            print(f"  • Has Arabic Characters: {'✅ YES' if has_arabic else '❌ NO'}")
            print(f"  • Has Quality Arabic Words: {'✅ YES' if has_quality_words else '❌ NO'}")
            print(f"  • Has Eid Context: {'✅ YES' if has_eid_content else '❌ NO'}")
            
            # Overall assessment
            if has_arabic and has_quality_words:
                print(f"\n✅ SUCCESS: Arabic content generated with cultural intelligence!")
                if has_eid_content:
                    print(f"🎉 BONUS: Eid cultural context properly included!")
            else:
                print(f"\n❌ ISSUE: Arabic content not properly generated!")
                
            # Save sample
            with open('quick_uae_sample.json', 'w', encoding='utf-8') as f:
                json.dump({
                    'title': title,
                    'bullets': bullets if isinstance(bullets, list) else [bullets],
                    'description': description,
                    'analysis': {
                        'has_arabic': has_arabic,
                        'has_quality_words': has_quality_words,
                        'has_eid_content': has_eid_content
                    }
                }, f, indent=2, ensure_ascii=False)
            
            print(f"\n📁 Sample saved to quick_uae_sample.json")
            
        else:
            print("❌ No listing generated")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        product.delete()

if __name__ == "__main__":
    quick_uae_test()