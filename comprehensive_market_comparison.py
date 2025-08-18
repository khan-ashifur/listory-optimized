"""
Comprehensive Market Comparison - Brazil, Mexico, Netherlands, Turkey
Analyzes A+ content, keywords, image strategy, and localization issues
Compares quality and identifies English content in non-English markets
"""

import os
import sys
import json
import django
from datetime import datetime

# Django setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from django.contrib.auth.models import User

def analyze_content_localization(content, expected_language, market_name):
    """Analyze content for localization issues"""
    issues = []
    
    # Common English words that shouldn't appear in other languages
    english_words = [
        'PRECISION BUILT', 'ULTIMATE', 'PREMIUM QUALITY', 'EXCEPTIONAL VALUE', 
        'SOPHISTICATED', 'FAMILY-SIZED', 'REFINED', 'LUXURY EXPERIENCE',
        'free shipping', 'customer service', 'warranty', 'guaranteed',
        'professional', 'high quality', 'best', 'perfect', 'excellent'
    ]
    
    for word in english_words:
        if word.lower() in content.lower():
            issues.append(f"English word '{word}' found in {market_name} content")
    
    return issues

def generate_market_listing(market_code, language, market_name, occasion):
    """Generate listing for specific market"""
    print(f"\n🌍 Generating {market_name} Market Listing...")
    print("=" * 50)
    
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username=f'{market_code}_test_user')
    
    # Create test product for this market
    product = Product.objects.create(
        user=test_user,
        name="Premium Kitchen Knife Set",
        description="Professional chef knife set with premium steel blades and ergonomic handles for home cooking",
        brand_name="ChefMaster",
        brand_tone="professional",
        target_platform="amazon",
        marketplace=market_code,
        marketplace_language=language,
        categories="Home/Kitchen/Knives",
        features="Sharp Blades, Ergonomic Handle, Professional Quality, Easy Maintenance, Complete Set",
        target_audience=f"{market_name} families who love cooking and appreciate quality kitchen tools",
        occasion=occasion
    )
    
    try:
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
            
            # Analyze content
            bullets_text = ' '.join(bullets) if isinstance(bullets, list) else str(bullets)
            full_content = f"{title} {bullets_text} {description} {keywords} {backend_keywords} {aplus_content}"
            
            # Check for localization issues
            localization_issues = analyze_content_localization(full_content, language, market_name)
            
            print(f"📊 {market_name} Market Analysis:")
            print(f"  • Title ({len(title)} chars): {title[:100]}...")
            print(f"  • Description ({len(description)} chars): {description[:150]}...")
            print(f"  • Keywords: {keywords[:100]}...")
            print(f"  • Backend Keywords: {backend_keywords[:100]}...")
            
            # Check bullets for English labels
            print(f"  • Bullet Point Labels:")
            for i, bullet in enumerate(bullets[:3]):
                if bullet and bullet.strip():
                    label = bullet.split(':')[0] if ':' in bullet else bullet[:20]
                    print(f"    - Bullet {i+1}: {label}")
            
            # Localization Issues
            print(f"  • Localization Issues: {len(localization_issues)}")
            for issue in localization_issues[:3]:
                print(f"    ⚠️ {issue}")
            
            # A+ Content Analysis
            if aplus_content:
                print(f"  • A+ Content ({len(aplus_content)} chars): Available")
                # Check for English in A+ content
                aplus_issues = analyze_content_localization(aplus_content, language, f"{market_name} A+ Content")
                if aplus_issues:
                    print(f"    ⚠️ A+ Content has {len(aplus_issues)} English issues")
            else:
                print(f"  • A+ Content: Missing")
            
            # Image Strategy Analysis (if available in A+ content)
            if 'image' in aplus_content.lower():
                print(f"  • Image Strategy: Found in A+ content")
                if any(word in aplus_content.lower() for word in ['image of', 'photo of', 'picture of']):
                    print(f"    ⚠️ Image descriptions might be in English")
            
            # Occasion Integration Check
            occasion_in_content = occasion.lower() in full_content.lower()
            print(f"  • Occasion Integration ({occasion}): {'✅' if occasion_in_content else '❌'}")
            
            # Brand Tone Consistency Check
            tone_words = {
                'professional': ['professional', 'expertise', 'industry', 'quality'],
                'luxury': ['premium', 'elegant', 'sophisticated', 'exclusive'],
                'casual': ['easy', 'simple', 'everyday', 'convenient'],
                'playful': ['fun', 'exciting', 'vibrant', 'colorful']
            }
            brand_tone = 'professional'  # Default for our test
            expected_tone_words = tone_words.get(brand_tone, [])
            tone_matches = sum(1 for word in expected_tone_words if word.lower() in full_content.lower())
            print(f"  • Brand Tone Consistency: {tone_matches}/{len(expected_tone_words)} matches")
            
            return {
                'market': market_name,
                'market_code': market_code,
                'language': language,
                'occasion': occasion,
                'occasion_integrated': occasion_in_content,
                'brand_tone_matches': tone_matches,
                'brand_tone_total': len(expected_tone_words),
                'title': title,
                'bullets': bullets,
                'description': description,
                'keywords': keywords,
                'backend_keywords': backend_keywords,
                'aplus_content': aplus_content,
                'localization_issues': localization_issues,
                'content_length': len(full_content),
                'quality_score': max(0, 10 - len(localization_issues))
            }
        
        else:
            print(f"❌ No listing generated for {market_name}")
            return None
            
    except Exception as e:
        print(f"❌ Error generating {market_name} listing: {str(e)}")
        return None
    
    finally:
        product.delete()

def comprehensive_market_comparison():
    print("\n🌟 COMPREHENSIVE MARKET COMPARISON")
    print("=" * 70)
    print("🎯 Testing: Brazil, Mexico, Netherlands, Turkey")
    print("🔍 Focus: A+ content, keywords, image strategy, localization")
    print("=" * 70)
    
    # Market configurations
    markets = [
        {
            'code': 'br',
            'language': 'pt-br', 
            'name': 'Brazil',
            'occasion': 'carnaval'
        },
        {
            'code': 'mx',
            'language': 'es-mx',
            'name': 'Mexico', 
            'occasion': 'dia_de_muertos'
        },
        {
            'code': 'nl',
            'language': 'nl',
            'name': 'Netherlands',
            'occasion': 'koningsdag'
        },
        {
            'code': 'tr',
            'language': 'tr',
            'name': 'Turkey',
            'occasion': 'kurban_bayrami'
        }
    ]
    
    results = []
    
    # Generate listings for each market
    for market in markets:
        result = generate_market_listing(
            market['code'], 
            market['language'], 
            market['name'], 
            market['occasion']
        )
        if result:
            results.append(result)
    
    # Comparative Analysis
    print(f"\n📊 COMPARATIVE ANALYSIS")
    print("=" * 50)
    
    for result in results:
        flag_map = {'br': '🇧🇷', 'mx': '🇲🇽', 'nl': '🇳🇱', 'tr': '🇹🇷'}
        flag = flag_map.get(result['market_code'], '🌍')
        
        print(f"\n{flag} {result['market']} ({result['market_code'].upper()}):")
        print(f"  • Quality Score: {result['quality_score']}/10")
        print(f"  • Localization Issues: {len(result['localization_issues'])}")
        print(f"  • Content Length: {result['content_length']} chars")
        print(f"  • Language: {result['language']}")
        print(f"  • Occasion ({result['occasion']}): {'✅ Integrated' if result['occasion_integrated'] else '❌ Missing'}")
        print(f"  • Brand Tone: {result['brand_tone_matches']}/{result['brand_tone_total']} consistency")
        
        # Top issues
        if result['localization_issues']:
            print(f"  • Top Issues:")
            for issue in result['localization_issues'][:2]:
                print(f"    - {issue}")
    
    # Save comprehensive comparison
    with open('comprehensive_market_comparison.json', 'w', encoding='utf-8') as f:
        json.dump({
            'comparison_date': datetime.now().isoformat(),
            'markets_tested': len(results),
            'results': results,
            'summary': {
                'best_quality': max(results, key=lambda x: x['quality_score'])['market'],
                'most_issues': max(results, key=lambda x: len(x['localization_issues']))['market'],
                'average_quality': sum(r['quality_score'] for r in results) / len(results),
                'total_issues': sum(len(r['localization_issues']) for r in results)
            }
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n📁 Comprehensive comparison saved to comprehensive_market_comparison.json")
    
    # Final recommendations
    print(f"\n🎯 RECOMMENDATIONS:")
    high_issues = [r for r in results if len(r['localization_issues']) > 5]
    if high_issues:
        print(f"  ⚠️ Markets needing immediate attention:")
        for market in high_issues:
            print(f"    - {market['market']}: {len(market['localization_issues'])} issues")
    
    print(f"  🔧 Common fixes needed:")
    print(f"    - Replace English bullet labels with local language")
    print(f"    - Translate image strategy descriptions")
    print(f"    - Use local keywords instead of English ones")
    print(f"    - Ensure A+ content is fully localized")

if __name__ == "__main__":
    comprehensive_market_comparison()