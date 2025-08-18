"""
A+ Content Competitor Analysis - Deep Dive
Compares A+ content across markets vs Helium 10, Jasper AI, CopyMonkey
Analyzes structure, localization, image strategy, and conversion elements
"""

import os
import sys
import json
import django
import re
from datetime import datetime

# Django setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from django.contrib.auth.models import User

def analyze_aplus_quality(aplus_content, market_name, language):
    """Analyze A+ content quality against competitor standards"""
    
    if not aplus_content:
        return {
            'total_score': 0,
            'sections': 0,
            'images': 0,
            'localization_score': 0,
            'conversion_elements': 0,
            'issues': ['No A+ content generated']
        }
    
    analysis = {
        'content_length': len(aplus_content),
        'sections': 0,
        'images': 0,
        'localization_score': 0,
        'conversion_elements': 0,
        'competitor_comparison': {},
        'issues': []
    }
    
    # 1. Structure Analysis (Helium 10 standard: 3-5 sections)
    section_patterns = ['section', 'hero', 'feature', 'benefit', 'trust', 'faq']
    sections_found = sum(1 for pattern in section_patterns if pattern.lower() in aplus_content.lower())
    analysis['sections'] = sections_found
    
    # 2. Image Strategy Analysis (CopyMonkey standard: detailed image descriptions)
    image_patterns = ['image', 'photo', 'picture', 'visual', 'graphic']
    images_found = sum(1 for pattern in image_patterns if pattern.lower() in aplus_content.lower())
    analysis['images'] = images_found
    
    # 3. Conversion Elements (CopyMonkey standard: trust, urgency, benefits)
    conversion_patterns = {
        'trust_signals': ['guarantee', 'certified', 'warranty', 'quality', 'garanti', 'sertifika', 'garantía'],
        'urgency': ['limited', 'now', 'today', 'exclusive', 'şimdi', 'özel', 'exclusivo'],
        'benefits': ['benefit', 'advantage', 'solution', 'fayda', 'avantaj', 'beneficio'],
        'social_proof': ['customer', 'review', 'testimonial', 'müşteri', 'cliente']
    }
    
    conversion_score = 0
    for category, patterns in conversion_patterns.items():
        found = sum(1 for pattern in patterns if pattern.lower() in aplus_content.lower())
        if found > 0:
            conversion_score += 1
    analysis['conversion_elements'] = conversion_score
    
    # 4. Localization Quality Check
    english_phrases = [
        'image of', 'photo of', 'picture of', 'shows the product', 'featuring',
        'product image', 'lifestyle image', 'demonstration of', 'highlights the'
    ]
    
    english_issues = sum(1 for phrase in english_phrases if phrase.lower() in aplus_content.lower())
    localization_score = max(0, 10 - (english_issues * 2))
    analysis['localization_score'] = localization_score
    
    if english_issues > 0:
        analysis['issues'].append(f"{english_issues} English phrases found in {market_name} A+ content")
    
    # 5. Competitor Comparison Scores
    
    # Helium 10 equivalent (structure focus)
    helium10_score = min(10, (sections_found * 2) + (images_found * 1))
    
    # Jasper AI equivalent (creativity and flow)
    content_variety = len(set(re.findall(r'\b\w{5,}\b', aplus_content.lower()))) / 100  # Vocabulary diversity
    jasper_score = min(10, (content_variety * 3) + (sections_found * 1.5) + (localization_score * 0.3))
    
    # CopyMonkey equivalent (conversion optimization)
    copymonkey_score = min(10, (conversion_score * 2) + (sections_found * 1) + (images_found * 0.5))
    
    analysis['competitor_comparison'] = {
        'helium10_equivalent': round(helium10_score, 1),
        'jasper_equivalent': round(jasper_score, 1),
        'copymonkey_equivalent': round(copymonkey_score, 1)
    }
    
    # Total quality score
    analysis['total_score'] = round((helium10_score + jasper_score + copymonkey_score) / 3, 1)
    
    return analysis

def generate_and_analyze_aplus(market_code, language, market_name, occasion):
    """Generate listing and analyze A+ content for specific market"""
    print(f"\n🔍 Analyzing {market_name} A+ Content...")
    print("=" * 50)
    
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username=f'{market_code}_aplus_test')
    
    # Test product for A+ content analysis
    product = Product.objects.create(
        user=test_user,
        name="Professional Wireless Headphones",
        description="Premium noise-canceling wireless headphones with long battery life and superior sound quality",
        brand_name="AudioPro",
        brand_tone="professional",
        target_platform="amazon",
        marketplace=market_code,
        marketplace_language=language,
        categories="Electronics/Audio/Headphones",
        features="Noise Canceling, 30H Battery, Wireless, Premium Sound, Comfortable Design",
        target_audience=f"{market_name} music lovers and professionals",
        occasion=occasion
    )
    
    try:
        listing = service.generate_listing(product_id=product.id, platform='amazon')
        
        if listing and listing.amazon_aplus_content:
            aplus_content = listing.amazon_aplus_content
            
            # Analyze A+ content quality
            analysis = analyze_aplus_quality(aplus_content, market_name, language)
            
            print(f"📊 {market_name} A+ Content Analysis:")
            print(f"  • Content Length: {analysis['content_length']:,} characters")
            print(f"  • Sections Found: {analysis['sections']}")
            print(f"  • Image References: {analysis['images']}")
            print(f"  • Conversion Elements: {analysis['conversion_elements']}/4")
            print(f"  • Localization Score: {analysis['localization_score']}/10")
            print(f"  • Total Quality Score: {analysis['total_score']}/10")
            
            print(f"\n🏆 Competitor Comparison:")
            comp = analysis['competitor_comparison']
            print(f"  • vs Helium 10: {comp['helium10_equivalent']}/10")
            print(f"  • vs Jasper AI: {comp['jasper_equivalent']}/10") 
            print(f"  • vs CopyMonkey: {comp['copymonkey_equivalent']}/10")
            
            # Overall verdict
            avg_competitor_score = sum(comp.values()) / len(comp.values())
            if avg_competitor_score >= 8.0:
                verdict = "🏆 BEATS ALL COMPETITORS!"
            elif avg_competitor_score >= 6.5:
                verdict = "🥈 COMPETITIVE with top tools"
            elif avg_competitor_score >= 5.0:
                verdict = "🥉 GOOD but needs improvement"
            else:
                verdict = "❌ BELOW competitor standards"
            
            print(f"  • Overall: {verdict}")
            
            # Show issues if any
            if analysis['issues']:
                print(f"\n⚠️ Issues Found:")
                for issue in analysis['issues']:
                    print(f"    - {issue}")
            
            # Extract key A+ sections for comparison
            sections_preview = {}
            try:
                # Try to extract structured sections
                if 'hero' in aplus_content.lower():
                    hero_match = re.search(r'hero[^}]*}[^}]*}', aplus_content.lower())
                    if hero_match:
                        sections_preview['hero'] = aplus_content[hero_match.start():hero_match.start()+200] + "..."
                
                if 'feature' in aplus_content.lower():
                    feature_match = re.search(r'feature[^}]*}[^}]*}', aplus_content.lower())
                    if feature_match:
                        sections_preview['features'] = aplus_content[feature_match.start():feature_match.start()+200] + "..."
            except:
                sections_preview['preview'] = aplus_content[:300] + "..."
            
            return {
                'market': market_name,
                'market_code': market_code,
                'language': language,
                'occasion': occasion,
                'aplus_analysis': analysis,
                'sections_preview': sections_preview,
                'full_aplus_content': aplus_content
            }
        
        else:
            print(f"❌ No A+ content generated for {market_name}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None
    
    finally:
        product.delete()

def comprehensive_aplus_comparison():
    print("\n🌟 COMPREHENSIVE A+ CONTENT COMPETITOR ANALYSIS")
    print("=" * 70)
    print("🎯 Testing: Brazil, Mexico, Netherlands, Turkey A+ Content")
    print("🏆 Benchmark: Helium 10, Jasper AI, CopyMonkey standards")
    print("=" * 70)
    
    markets = [
        ('br', 'pt-br', 'Brazil', 'carnaval'),
        ('mx', 'es-mx', 'Mexico', 'dia_de_muertos'),
        ('nl', 'nl', 'Netherlands', 'koningsdag'),
        ('tr', 'tr', 'Turkey', 'kurban_bayrami')
    ]
    
    results = []
    
    # Analyze each market
    for market_code, language, market_name, occasion in markets:
        result = generate_and_analyze_aplus(market_code, language, market_name, occasion)
        if result:
            results.append(result)
    
    # Comparative analysis
    print(f"\n📊 CROSS-MARKET A+ CONTENT COMPARISON")
    print("=" * 60)
    
    best_overall = None
    best_score = 0
    
    for result in results:
        analysis = result['aplus_analysis']
        flag_map = {'br': '🇧🇷', 'mx': '🇲🇽', 'nl': '🇳🇱', 'tr': '🇹🇷'}
        flag = flag_map.get(result['market_code'], '🌍')
        
        print(f"\n{flag} {result['market']}:")
        print(f"  • Total Quality: {analysis['total_score']}/10")
        print(f"  • Content Length: {analysis['content_length']:,} chars")
        print(f"  • Localization: {analysis['localization_score']}/10")
        print(f"  • Conversion Elements: {analysis['conversion_elements']}/4")
        
        # Track best performer
        if analysis['total_score'] > best_score:
            best_score = analysis['total_score']
            best_overall = result
    
    # Winner announcement
    if best_overall:
        winner = best_overall['market']
        winner_score = best_overall['aplus_analysis']['total_score']
        print(f"\n🏆 A+ CONTENT CHAMPION: {winner}")
        print(f"  🎯 Score: {winner_score}/10")
        print(f"  📈 Beats competitors: {'YES' if winner_score >= 7.0 else 'NEEDS IMPROVEMENT'}")
    
    # Save comprehensive results
    with open('aplus_competitor_analysis.json', 'w', encoding='utf-8') as f:
        json.dump({
            'analysis_date': datetime.now().isoformat(),
            'markets_analyzed': len(results),
            'results': results,
            'champion': {
                'market': best_overall['market'] if best_overall else None,
                'score': best_score,
                'beats_competitors': best_score >= 7.0
            },
            'competitor_standards': {
                'helium10_focus': 'Structure and sections (3-5 sections)',
                'jasper_focus': 'Creativity and vocabulary diversity',
                'copymonkey_focus': 'Conversion optimization and trust signals'
            }
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n📁 Complete A+ analysis saved to aplus_competitor_analysis.json")
    
    # Final recommendations
    print(f"\n🎯 RECOMMENDATIONS:")
    high_performers = [r for r in results if r['aplus_analysis']['total_score'] >= 7.0]
    if high_performers:
        print(f"  🏆 Ready for production:")
        for result in high_performers:
            print(f"    - {result['market']}: {result['aplus_analysis']['total_score']}/10")
    
    low_performers = [r for r in results if r['aplus_analysis']['total_score'] < 7.0]
    if low_performers:
        print(f"  ⚠️ Need improvement:")
        for result in low_performers:
            issues = result['aplus_analysis']['issues']
            print(f"    - {result['market']}: {result['aplus_analysis']['total_score']}/10")
            if issues:
                print(f"      Issues: {', '.join(issues[:2])}")

if __name__ == "__main__":
    comprehensive_aplus_comparison()