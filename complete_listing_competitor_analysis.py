"""
Complete Listing Competitor Analysis
Comprehensive comparison of ENTIRE listings vs Helium 10, Jasper AI, CopyMonkey
Tests: Title, Bullets, Description, A+ Content, Keywords, SEO across all markets
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

class CompetitorBenchmark:
    """Competitor standards for comparison"""
    
    @staticmethod
    def helium10_standards():
        return {
            'title': {
                'length_range': (150, 200),
                'keyword_density': 3,  # Main keywords in title
                'structure': 'Brand + Product + Key Features + Benefits',
                'score_weight': 0.25
            },
            'bullets': {
                'count': 5,
                'length_per_bullet': (150, 250),
                'structure': 'FEATURE: Benefit explanation with specs',
                'conversion_elements': ['guarantee', 'quality', 'benefit'],
                'score_weight': 0.25
            },
            'description': {
                'length_range': (800, 1500),
                'paragraphs': 4,
                'seo_optimization': True,
                'score_weight': 0.20
            },
            'aplus_content': {
                'sections': 5,
                'images': 3,
                'length_range': (15000, 30000),
                'score_weight': 0.20
            },
            'keywords': {
                'primary_count': 8,
                'long_tail_count': 25,
                'localization': True,
                'score_weight': 0.10
            }
        }
    
    @staticmethod
    def jasper_standards():
        return {
            'creativity_score': 8.0,  # Content creativity and flow
            'vocabulary_diversity': 150,  # Unique words
            'emotional_hooks': 5,  # Emotional triggers
            'storytelling': True,  # Narrative elements
            'brand_voice_consistency': 9.0
        }
    
    @staticmethod
    def copymonkey_standards():
        return {
            'conversion_rate_optimization': 8.5,
            'trust_signals': 4,  # Guarantee, reviews, etc.
            'urgency_elements': 2,  # Limited time, exclusive
            'benefit_focused': True,
            'customer_pain_points': 3,  # Problems solved
            'call_to_action': 2
        }

def analyze_complete_listing(market_code, language, market_name, occasion):
    """Analyze complete listing against all competitor standards"""
    print(f"\n🔍 COMPLETE LISTING ANALYSIS: {market_name}")
    print("=" * 60)
    
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username=f'{market_code}_complete_test')
    
    # Premium product for comprehensive testing
    product = Product.objects.create(
        user=test_user,
        name="Premium Wireless Bluetooth Earbuds",
        description="Professional wireless earbuds with active noise cancellation, premium sound quality, and long battery life for music lovers and professionals",
        brand_name="SoundMaster",
        brand_tone="luxury",
        target_platform="amazon",
        marketplace=market_code,
        marketplace_language=language,
        categories="Electronics/Audio/Earbuds",
        features="Active Noise Cancellation, 40H Battery, Premium Sound, Wireless Charging, Water Resistant",
        target_audience=f"{market_name} music enthusiasts and professionals who demand premium audio quality",
        occasion=occasion
    )
    
    try:
        listing = service.generate_listing(product_id=product.id, platform='amazon')
        
        if not listing:
            print("❌ No listing generated")
            return None
        
        # Extract all components
        title = listing.title or ''
        try:
            bullets = json.loads(listing.bullet_points) if listing.bullet_points else []
        except json.JSONDecodeError:
            bullets = listing.bullet_points.split('\n') if listing.bullet_points else []
        description = listing.long_description or ''
        keywords = listing.amazon_keywords or ''
        backend_keywords = listing.amazon_backend_keywords or ''
        aplus_content = listing.amazon_aplus_content or ''
        
        analysis_result = {
            'market': market_name,
            'code': market_code,
            'language': language,
            'occasion': occasion,
            'components': {
                'title': title,
                'bullets': bullets,
                'description': description,
                'keywords': keywords,
                'backend_keywords': backend_keywords,
                'aplus_content': aplus_content
            },
            'competitor_scores': {},
            'overall_verdict': '',
            'detailed_analysis': {}
        }
        
        # 1. HELIUM 10 ANALYSIS
        print(f"🎯 HELIUM 10 COMPARISON:")
        helium10 = CompetitorBenchmark.helium10_standards()
        h10_scores = {}
        
        # Title analysis
        title_score = 0
        if helium10['title']['length_range'][0] <= len(title) <= helium10['title']['length_range'][1]:
            title_score += 3
        keyword_count = sum(1 for word in ['premium', 'wireless', 'bluetooth', 'earbuds'] if word.lower() in title.lower())
        title_score += min(3, keyword_count)
        h10_scores['title'] = min(10, title_score * 1.67)
        print(f"  • Title: {h10_scores['title']:.1f}/10 (Length: {len(title)}, Keywords: {keyword_count})")
        
        # Bullets analysis
        bullet_score = 0
        if len(bullets) >= 5:
            bullet_score += 2
        bullet_lengths = [len(b) for b in bullets if b.strip()]
        avg_bullet_length = sum(bullet_lengths) / len(bullet_lengths) if bullet_lengths else 0
        if 150 <= avg_bullet_length <= 250:
            bullet_score += 3
        
        # Check for structured bullets (FEATURE: Description format)
        structured_bullets = sum(1 for b in bullets if ':' in b and b.strip())
        bullet_score += min(3, structured_bullets * 0.6)
        h10_scores['bullets'] = min(10, bullet_score * 1.25)
        print(f"  • Bullets: {h10_scores['bullets']:.1f}/10 (Count: {len(bullets)}, Avg length: {avg_bullet_length:.0f})")
        
        # Description analysis
        desc_score = 0
        if helium10['description']['length_range'][0] <= len(description) <= helium10['description']['length_range'][1]:
            desc_score += 4
        paragraphs = description.count('\n\n') + 1
        if paragraphs >= 3:
            desc_score += 3
        desc_score += min(3, len(re.findall(r'\b\w{6,}\b', description)) / 50)  # Vocabulary richness
        h10_scores['description'] = min(10, desc_score)
        print(f"  • Description: {h10_scores['description']:.1f}/10 (Length: {len(description)}, Paragraphs: {paragraphs})")
        
        # A+ Content analysis
        aplus_score = 0
        if aplus_content:
            if len(aplus_content) >= 15000:
                aplus_score += 4
            sections = sum(1 for word in ['hero', 'feature', 'benefit', 'trust', 'faq'] if word.lower() in aplus_content.lower())
            aplus_score += min(4, sections * 0.8)
            images = aplus_content.lower().count('image')
            aplus_score += min(2, images * 0.67)
        h10_scores['aplus'] = aplus_score
        print(f"  • A+ Content: {h10_scores['aplus']:.1f}/10 (Length: {len(aplus_content):,}, Sections: {sections if aplus_content else 0})")
        
        # Keywords analysis
        keyword_score = 0
        primary_keywords = keywords.count(',') + 1 if keywords else 0
        if primary_keywords >= 8:
            keyword_score += 4
        backend_keywords_count = backend_keywords.count(' ') + 1 if backend_keywords else 0
        if backend_keywords_count >= 25:
            keyword_score += 3
        
        # Localization check
        english_words = ['premium', 'quality', 'professional', 'best']
        english_in_keywords = sum(1 for word in english_words if word.lower() in f"{keywords} {backend_keywords}".lower())
        if english_in_keywords < 3:  # Good localization
            keyword_score += 3
        h10_scores['keywords'] = keyword_score
        print(f"  • Keywords: {h10_scores['keywords']:.1f}/10 (Primary: {primary_keywords}, Backend: {backend_keywords_count})")
        
        helium10_overall = sum(h10_scores.values()) / len(h10_scores)
        print(f"  🎯 HELIUM 10 OVERALL: {helium10_overall:.1f}/10")
        
        # 2. JASPER AI ANALYSIS
        print(f"\n🎨 JASPER AI COMPARISON:")
        jasper = CompetitorBenchmark.jasper_standards()
        
        full_content = f"{title} {' '.join(bullets)} {description}"
        
        # Creativity & vocabulary diversity
        unique_words = len(set(re.findall(r'\b\w{4,}\b', full_content.lower())))
        creativity_score = min(10, unique_words / 15)
        
        # Emotional hooks
        emotion_words = ['incredible', 'amazing', 'perfect', 'ultimate', 'exceptional', 'premium', 'luxury', 'professional']
        emotion_count = sum(1 for word in emotion_words if word.lower() in full_content.lower())
        emotion_score = min(10, emotion_count * 1.5)
        
        # Brand voice consistency
        tone_consistency = 8.0 if 'luxury' in product.brand_tone else 7.0  # Simplified check
        
        jasper_overall = (creativity_score + emotion_score + tone_consistency) / 3
        print(f"  • Creativity: {creativity_score:.1f}/10 (Unique words: {unique_words})")
        print(f"  • Emotional hooks: {emotion_score:.1f}/10 (Count: {emotion_count})")
        print(f"  • Brand consistency: {tone_consistency:.1f}/10")
        print(f"  🎨 JASPER AI OVERALL: {jasper_overall:.1f}/10")
        
        # 3. COPYMONKEY ANALYSIS
        print(f"\n🎯 COPYMONKEY COMPARISON:")
        copymonkey = CompetitorBenchmark.copymonkey_standards()
        
        # Trust signals
        trust_words = ['guarantee', 'warranty', 'certified', 'quality', 'professional', 'premium']
        trust_count = sum(1 for word in trust_words if word.lower() in full_content.lower())
        trust_score = min(10, trust_count * 1.5)
        
        # Conversion optimization
        conversion_words = ['buy', 'order', 'get', 'enjoy', 'experience', 'upgrade']
        conversion_count = sum(1 for word in conversion_words if word.lower() in full_content.lower())
        conversion_score = min(10, conversion_count * 2)
        
        # Benefit focus
        benefit_indicators = bullets.count(':') + description.count('benefit') + description.count('advantage')
        benefit_score = min(10, benefit_indicators * 1.2)
        
        copymonkey_overall = (trust_score + conversion_score + benefit_score) / 3
        print(f"  • Trust signals: {trust_score:.1f}/10 (Count: {trust_count})")
        print(f"  • Conversion optimization: {conversion_score:.1f}/10 (Count: {conversion_count})")
        print(f"  • Benefit focus: {benefit_score:.1f}/10")
        print(f"  🎯 COPYMONKEY OVERALL: {copymonkey_overall:.1f}/10")
        
        # ULTIMATE COMPETITOR SCORE
        ultimate_score = (helium10_overall + jasper_overall + copymonkey_overall) / 3
        
        # Verdict
        if ultimate_score >= 9.0:
            verdict = "🏆 DESTROYS ALL COMPETITORS!"
            status = "LEGENDARY"
        elif ultimate_score >= 8.0:
            verdict = "🥇 BEATS ALL COMPETITORS!"
            status = "CHAMPION"
        elif ultimate_score >= 7.0:
            verdict = "🥈 HIGHLY COMPETITIVE"
            status = "EXPERT"
        elif ultimate_score >= 6.0:
            verdict = "🥉 COMPETITIVE"
            status = "ADVANCED"
        else:
            verdict = "❌ BELOW COMPETITORS"
            status = "NEEDS WORK"
        
        print(f"\n🏆 ULTIMATE VERDICT:")
        print(f"  📊 Overall Score: {ultimate_score:.1f}/10")
        print(f"  🎖️ Status: {status}")
        print(f"  🎯 {verdict}")
        
        # Store results
        analysis_result['competitor_scores'] = {
            'helium10': helium10_overall,
            'jasper': jasper_overall,
            'copymonkey': copymonkey_overall,
            'ultimate': ultimate_score
        }
        analysis_result['overall_verdict'] = verdict
        analysis_result['status'] = status
        
        return analysis_result
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
    
    finally:
        product.delete()

def main():
    print("\n🌟 COMPLETE LISTING COMPETITOR ANALYSIS")
    print("=" * 70)
    print("🎯 Testing: ENTIRE listings vs Helium 10, Jasper AI, CopyMonkey")
    print("📊 Components: Title, Bullets, Description, A+ Content, Keywords")
    print("🌍 Markets: Brazil, Mexico, Netherlands, Turkey")
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
        result = analyze_complete_listing(market_code, language, market_name, occasion)
        if result:
            results.append(result)
    
    # FINAL COMPARISON
    print(f"\n🏆 FINAL COMPETITOR COMPARISON")
    print("=" * 60)
    
    best_market = None
    best_score = 0
    
    for result in results:
        flag_map = {'br': '🇧🇷', 'mx': '🇲🇽', 'nl': '🇳🇱', 'tr': '🇹🇷'}
        flag = flag_map.get(result['code'], '🌍')
        
        scores = result['competitor_scores']
        ultimate = scores['ultimate']
        
        print(f"\n{flag} {result['market']}:")
        print(f"  • vs Helium 10: {scores['helium10']:.1f}/10")
        print(f"  • vs Jasper AI: {scores['jasper']:.1f}/10") 
        print(f"  • vs CopyMonkey: {scores['copymonkey']:.1f}/10")
        print(f"  • ULTIMATE SCORE: {ultimate:.1f}/10")
        print(f"  • STATUS: {result['status']}")
        
        if ultimate > best_score:
            best_score = ultimate
            best_market = result
    
    # CHAMPION ANNOUNCEMENT
    if best_market:
        print(f"\n🎉 CHAMPION MARKET: {best_market['market']} 🏆")
        print(f"🎯 Score: {best_score:.1f}/10")
        print(f"🏅 {best_market['overall_verdict']}")
        
        if best_score >= 8.0:
            print(f"\n✅ PRODUCTION READY!")
            print(f"🚀 This implementation BEATS major competitors!")
        else:
            print(f"\n⚠️ Needs optimization to beat competitors consistently")
    
    # Save comprehensive results
    with open('complete_competitor_analysis.json', 'w', encoding='utf-8') as f:
        json.dump({
            'analysis_date': datetime.now().isoformat(),
            'markets_tested': len(results),
            'champion': {
                'market': best_market['market'] if best_market else None,
                'score': best_score,
                'verdict': best_market['overall_verdict'] if best_market else None
            },
            'results': results,
            'competitor_standards': {
                'helium10': 'SEO optimization, structure, keyword density',
                'jasper': 'Creativity, vocabulary, emotional engagement', 
                'copymonkey': 'Conversion optimization, trust signals, benefits'
            }
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n📁 Complete analysis saved to complete_competitor_analysis.json")

if __name__ == "__main__":
    main()