"""
Turkey Market Localization Issues Test
Specifically checks for English bullet labels, keywords, and A+ content issues
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

def turkey_localization_test():
    print("\n🇹🇷 TURKEY MARKET LOCALIZATION ISSUES TEST")
    print("=" * 60)
    print("🔍 Checking: Bullet labels, Keywords, A+ content, Image strategy")
    print("=" * 60)
    
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username='turkey_localization_test')
    
    # Create test product for Turkey market
    product = Product.objects.create(
        user=test_user,
        name="Premium Turkish Tea Glass Set",
        description="Traditional Turkish tea glasses with authentic design for family gatherings and guest hospitality",
        brand_name="ÇayMaster",
        brand_tone="luxury",
        target_platform="amazon",
        marketplace="tr",
        marketplace_language="tr",
        categories="Home/Kitchen/Drinkware",
        features="Traditional Design, Heat Resistant, Elegant Shape, Family Size, Gift Ready",
        target_audience="Turkish families who value traditional tea culture and hospitality",
        occasion="kurban_bayrami"
    )
    
    try:
        print("⏳ Generating Turkish listing...")
        listing = service.generate_listing(product_id=product.id, platform='amazon')
        
        if listing:
            title = listing.title or ''
            try:
                bullets = json.loads(listing.bullet_points) if listing.bullet_points else []
            except json.JSONDecodeError:
                bullets = listing.bullet_points.split('\n') if listing.bullet_points else []
            description = listing.long_description or ''
            keywords = listing.amazon_keywords or ''
            backend_keywords = listing.amazon_backend_keywords or ''
            aplus_content = listing.amazon_aplus_content or ''
            
            print(f"\n📊 DETAILED LOCALIZATION ANALYSIS:")
            
            # 1. BULLET POINT LABELS ANALYSIS
            print(f"\n🎯 BULLET POINT LABELS CHECK:")
            english_labels_found = []
            for i, bullet in enumerate(bullets[:5]):
                if bullet and bullet.strip():
                    # Extract label (everything before first colon)
                    if ':' in bullet:
                        label = bullet.split(':')[0].strip()
                        print(f"  Bullet {i+1} Label: '{label}'")
                        
                        # Check if label is in English
                        english_label_patterns = [
                            'PREMIUM QUALITY', 'LUXURY EXPERIENCE', 'EXCEPTIONAL VALUE',
                            'SOPHISTICATED', 'FAMILY-SIZED', 'REFINED', 'PRECISION BUILT'
                        ]
                        if any(pattern in label.upper() for pattern in english_label_patterns):
                            english_labels_found.append(f"Bullet {i+1}: {label}")
                            print(f"    ❌ ENGLISH LABEL DETECTED!")
                        else:
                            print(f"    ✅ Turkish label")
                    else:
                        print(f"  Bullet {i+1}: No label format detected")
            
            # 2. KEYWORDS ANALYSIS
            print(f"\n🔍 KEYWORDS ANALYSIS:")
            print(f"  Frontend Keywords: {keywords[:150]}...")
            print(f"  Backend Keywords: {backend_keywords[:150]}...")
            
            # Check for English keywords
            english_keywords = []
            all_keywords = f"{keywords} {backend_keywords}".lower()
            english_patterns = ['premium kitchen', 'high quality', 'best', 'professional', 'excellent']
            for pattern in english_patterns:
                if pattern in all_keywords:
                    english_keywords.append(pattern)
            
            if english_keywords:
                print(f"  ❌ English keywords found: {english_keywords}")
            else:
                print(f"  ✅ Keywords appear to be in Turkish")
            
            # 3. A+ CONTENT ANALYSIS
            print(f"\n📄 A+ CONTENT ANALYSIS:")
            if aplus_content:
                print(f"  A+ Content Length: {len(aplus_content)} characters")
                
                # Check for English in A+ content
                aplus_english_issues = []
                english_phrases = ['image of', 'photo of', 'picture of', 'shows', 'featuring', 'product image']
                for phrase in english_phrases:
                    if phrase.lower() in aplus_content.lower():
                        aplus_english_issues.append(phrase)
                
                if aplus_english_issues:
                    print(f"  ❌ English phrases in A+ content: {aplus_english_issues}")
                else:
                    print(f"  ✅ A+ content appears to be in Turkish")
                    
                # Check for image strategy descriptions
                if 'image' in aplus_content.lower():
                    print(f"  🖼️ Image strategy found in A+ content")
                    # Extract image descriptions
                    import re
                    image_matches = re.findall(r'["\']image[^"\']*["\']', aplus_content.lower())
                    for match in image_matches[:3]:
                        print(f"    Image desc: {match}")
                else:
                    print(f"  ⚠️ No image strategy found")
            else:
                print(f"  ❌ No A+ content generated")
            
            # 4. OCCASION INTEGRATION
            print(f"\n🎊 OCCASION INTEGRATION:")
            occasion_words = ['kurban', 'bayram', 'bayramı']
            occasion_found = any(word in f"{title} {description}".lower() for word in occasion_words)
            print(f"  Kurban Bayramı integration: {'✅' if occasion_found else '❌'}")
            
            # 5. BRAND TONE CONSISTENCY
            print(f"\n🎨 BRAND TONE ANALYSIS (Luxury):")
            luxury_words_turkish = ['premium', 'lüks', 'zarif', 'şık', 'kaliteli', 'özel']
            luxury_count = sum(1 for word in luxury_words_turkish if word.lower() in f"{title} {description}".lower())
            print(f"  Turkish luxury words found: {luxury_count}/6")
            
            # SUMMARY
            print(f"\n📋 LOCALIZATION ISSUES SUMMARY:")
            total_issues = len(english_labels_found) + len(english_keywords) + len(aplus_english_issues)
            print(f"  • English bullet labels: {len(english_labels_found)}")
            print(f"  • English keywords: {len(english_keywords)}")
            print(f"  • English A+ content phrases: {len(aplus_english_issues)}")
            print(f"  • Total localization issues: {total_issues}")
            
            if total_issues == 0:
                print(f"  🎉 PERFECT LOCALIZATION!")
            elif total_issues <= 3:
                print(f"  ⚠️ Minor localization issues")
            else:
                print(f"  ❌ MAJOR localization issues need fixing")
            
            # Save detailed analysis
            analysis_result = {
                'title': title,
                'bullets': bullets,
                'keywords': keywords,
                'backend_keywords': backend_keywords,
                'aplus_content_length': len(aplus_content),
                'localization_issues': {
                    'english_bullet_labels': english_labels_found,
                    'english_keywords': english_keywords,
                    'english_aplus_phrases': aplus_english_issues,
                    'total_issues': total_issues
                },
                'occasion_integrated': occasion_found,
                'luxury_tone_score': luxury_count
            }
            
            with open('turkey_localization_analysis.json', 'w', encoding='utf-8') as f:
                json.dump(analysis_result, f, indent=2, ensure_ascii=False)
            
            print(f"\n📁 Detailed analysis saved to turkey_localization_analysis.json")
            
        else:
            print("❌ No listing generated")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        product.delete()

if __name__ == "__main__":
    turkey_localization_test()