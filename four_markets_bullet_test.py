"""
Quick Four Markets Bullet Labels Test
Tests Brazil, Mexico, Netherlands, Turkey for English bullet labels specifically
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

def test_market_bullets(market_code, language, market_name, occasion):
    """Test bullet labels for a specific market"""
    print(f"\n{market_name.upper()} MARKET TEST:")
    print("-" * 30)
    
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username=f'{market_code}_bullet_test')
    
    product = Product.objects.create(
        user=test_user,
        name="Premium Coffee Maker",
        description="Professional coffee maker for home use",
        brand_name="CoffeePro",
        brand_tone="professional",
        target_platform="amazon",
        marketplace=market_code,
        marketplace_language=language,
        categories="Home/Kitchen/Coffee",
        features="Automatic, Easy Clean, Timer, Strong Coffee",
        target_audience=f"{market_name} coffee lovers",
        occasion=occasion
    )
    
    try:
        listing = service.generate_listing(product_id=product.id, platform='amazon')
        
        if listing:
            try:
                bullets = json.loads(listing.bullet_points) if listing.bullet_points else []
            except json.JSONDecodeError:
                bullets = listing.bullet_points.split('\n') if listing.bullet_points else []
            
            print(f"Bullet Labels Analysis:")
            english_issues = 0
            
            for i, bullet in enumerate(bullets[:3]):
                if bullet and bullet.strip():
                    if ':' in bullet:
                        label = bullet.split(':')[0].strip()
                        print(f"  • Bullet {i+1}: '{label}'")
                        
                        # Check for English patterns
                        english_patterns = ['PREMIUM QUALITY', 'LUXURY EXPERIENCE', 'EXCEPTIONAL VALUE', 
                                          'SOPHISTICATED', 'FAMILY-SIZED', 'REFINED', 'PRECISION BUILT',
                                          'ULTIMATE', 'PERFECT', 'INCREDIBLE']
                        
                        is_english = any(pattern in label.upper() for pattern in english_patterns)
                        if is_english:
                            print(f"    ❌ ENGLISH DETECTED!")
                            english_issues += 1
                        else:
                            print(f"    ✅ Local language")
                    
            # Check keywords quickly
            keywords = listing.amazon_keywords or ''
            english_keywords = sum(1 for word in ['premium', 'quality', 'professional', 'best'] 
                                 if word.lower() in keywords.lower())
            
            print(f"Quick Summary:")
            print(f"  • English bullet labels: {english_issues}")
            print(f"  • English keywords detected: {english_keywords}")
            print(f"  • Overall status: {'✅ GOOD' if english_issues == 0 else '❌ NEEDS FIX'}")
            
            return {
                'market': market_name,
                'code': market_code,
                'english_bullets': english_issues,
                'english_keywords': english_keywords,
                'status': 'GOOD' if english_issues == 0 else 'NEEDS_FIX'
            }
        
        else:
            print("❌ No listing generated")
            return None
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None
    
    finally:
        product.delete()

def main():
    print("🌍 FOUR MARKETS BULLET LABELS TEST")
    print("=" * 50)
    
    markets = [
        ('br', 'pt-br', 'Brazil', 'carnaval'),
        ('mx', 'es-mx', 'Mexico', 'dia_de_muertos'), 
        ('nl', 'nl', 'Netherlands', 'koningsdag'),
        ('tr', 'tr', 'Turkey', 'kurban_bayrami')
    ]
    
    results = []
    for market_code, language, market_name, occasion in markets:
        result = test_market_bullets(market_code, language, market_name, occasion)
        if result:
            results.append(result)
    
    print(f"\n📊 SUMMARY COMPARISON:")
    print("=" * 50)
    
    for result in results:
        flag_map = {'br': '🇧🇷', 'mx': '🇲🇽', 'nl': '🇳🇱', 'tr': '🇹🇷'}
        flag = flag_map.get(result['code'], '🌍')
        status_icon = '✅' if result['status'] == 'GOOD' else '❌'
        
        print(f"{flag} {result['market']}: {status_icon} {result['status']}")
        print(f"   English bullets: {result['english_bullets']}, English keywords: {result['english_keywords']}")
    
    # Best vs worst
    good_markets = [r for r in results if r['status'] == 'GOOD']
    bad_markets = [r for r in results if r['status'] == 'NEEDS_FIX']
    
    print(f"\n🏆 BEST PERFORMING:")
    for market in good_markets:
        print(f"  ✅ {market['market']} - Perfect localization")
    
    if bad_markets:
        print(f"\n⚠️ NEEDS IMPROVEMENT:")
        for market in bad_markets:
            print(f"  ❌ {market['market']} - {market['english_bullets']} English bullets")

if __name__ == "__main__":
    main()