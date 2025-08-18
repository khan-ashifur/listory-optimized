"""
Comprehensive Japan Market Test - Complete Validation
Tests Japan market with Japanese cultural nuances and character encoding
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

class JapanMarketTester:
    """Comprehensive Japan market testing with cultural validation"""
    
    def __init__(self):
        self.service = ListingGeneratorService()
        self.test_user, _ = User.objects.get_or_create(username='japan_tester')
        
        # Japanese test configurations
        self.japan_occasions = [
            'oshogatsu',      # New Year (most important)
            'kurisumasu',     # Christmas  
            'haha_no_hi',     # Mother's Day
            'ochutgen',       # Mid-year gift giving
            'oseibo',         # End-year gift giving
            'general'         # General occasion
        ]
        
        self.brand_tones = ['professional', 'luxurious', 'trustworthy']
        
        # Test products with Japanese market appeal
        self.test_products = [
            {
                'name': 'Premium Wireless Headphones',
                'category': 'Electronics/Audio/Headphones',
                'description': 'High-quality noise cancelling headphones with long battery life',
                'target': 'Professionals and commuters'
            },
            {
                'name': 'Smart Rice Cooker',
                'category': 'Home/Kitchen/Appliances', 
                'description': 'Advanced rice cooker with AI technology for perfect rice every time',
                'target': 'Families and cooking enthusiasts'
            },
            {
                'name': 'Portable Air Purifier',
                'category': 'Home/Health/Air Quality',
                'description': 'Compact air purifier with HEPA filter for clean, healthy air',
                'target': 'Health-conscious individuals'
            }
        ]
    
    def analyze_japanese_content(self, content):
        """Analyze content for Japanese language quality"""
        if not content:
            return {
                'has_japanese': False,
                'character_types': [],
                'politeness_level': 0,
                'quality_words': 0,
                'respect_words': 0
            }
        
        analysis = {
            'has_japanese': False,
            'character_types': [],
            'politeness_level': 0,
            'quality_words': 0,
            'respect_words': 0,
            'safety_words': 0
        }
        
        # Check for Japanese character types
        has_hiragana = any('\u3040' <= char <= '\u309F' for char in content)
        has_katakana = any('\u30A0' <= char <= '\u30FF' for char in content)
        has_kanji = any('\u4E00' <= char <= '\u9FFF' for char in content)
        
        if has_hiragana:
            analysis['character_types'].append('Hiragana')
        if has_katakana:
            analysis['character_types'].append('Katakana')
        if has_kanji:
            analysis['character_types'].append('Kanji')
        
        analysis['has_japanese'] = bool(analysis['character_types'])
        
        # Check for politeness indicators
        politeness_markers = ['です', 'ます', 'いたします', 'ございます', 'お客様', '皆様']
        analysis['politeness_level'] = sum(1 for marker in politeness_markers if marker in content)
        
        # Check for quality words
        quality_words = ['高品質', '品質', '安心', '信頼', '保証', '安全', 'プレミアム', '最高']
        analysis['quality_words'] = sum(1 for word in quality_words if word in content)
        
        # Check for respect words
        respect_words = ['お客様', '皆様', 'いただき', 'させていただき']
        analysis['respect_words'] = sum(1 for word in respect_words if word in content)
        
        # Check for safety/security words (important in Japan)
        safety_words = ['安心', '安全', '保証', '認証', 'PSE', '検査済み']
        analysis['safety_words'] = sum(1 for word in safety_words if word in content)
        
        return analysis
    
    def test_japan_market(self):
        """Run comprehensive Japan market test"""
        
        print("\n" + "="*80)
        print("🇯🇵 COMPREHENSIVE JAPAN MARKET TEST - LISTORY AI")
        print("Cultural Intelligence & Language Quality Validation")
        print("="*80)
        
        overall_results = []
        
        for product_config in self.test_products:
            print(f"\n\n{'='*60}")
            print(f"Testing Product: {product_config['name']}")
            print(f"Category: {product_config['category']}")
            print(f"{'='*60}")
            
            for occasion in self.japan_occasions:
                for tone in self.brand_tones:
                    print(f"\n🧪 Testing: {occasion.upper()} + {tone.upper()}")
                    print("-" * 50)
                    
                    # Create test product
                    product = Product.objects.create(
                        user=self.test_user,
                        name=product_config['name'],
                        description=product_config['description'],
                        brand_name="TestBrand",
                        brand_tone=tone,
                        target_platform="amazon",
                        marketplace="jp",  # Japan marketplace
                        marketplace_language="ja",  # Japanese language - CRITICAL!
                        categories=product_config['category'],
                        features="High Quality, Japanese Safety Standards, Premium Design",
                        target_audience=product_config['target'],
                        occasion=occasion
                    )
                    
                    try:
                        # Generate listing
                        listing = self.service.generate_listing(
                            product_id=product.id,
                            platform='amazon'
                        )
                        
                        if listing:
                            # Analyze generated content
                            title = listing.title or ''
                            bullets = json.loads(listing.bullet_points) if listing.bullet_points else []
                            description = listing.long_description or ''
                            
                            # Combine all text for analysis
                            full_text = f"{title} {' '.join(bullets)} {description}"
                            
                            # Analyze Japanese content quality
                            jp_analysis = self.analyze_japanese_content(full_text)
                            
                            # Results
                            result = {
                                'product': product_config['name'],
                                'occasion': occasion,
                                'tone': tone,
                                'title_length': len(title),
                                'bullet_count': len(bullets),
                                'description_length': len(description),
                                'japanese_analysis': jp_analysis,
                                'has_proper_encoding': jp_analysis['has_japanese'],
                                'cultural_score': self.calculate_cultural_score(jp_analysis)
                            }
                            
                            # Display results
                            print(f"  📊 Content Generation:")
                            print(f"    • Title: {result['title_length']} chars")
                            print(f"    • Bullets: {result['bullet_count']} points")
                            print(f"    • Description: {result['description_length']} chars")
                            
                            print(f"  🇯🇵 Japanese Quality:")
                            if jp_analysis['has_japanese']:
                                print(f"    • ✅ Character Types: {', '.join(jp_analysis['character_types'])}")
                                print(f"    • ✅ Politeness Level: {jp_analysis['politeness_level']}/6")
                                print(f"    • ✅ Quality Words: {jp_analysis['quality_words']}")
                                print(f"    • ✅ Respect Words: {jp_analysis['respect_words']}")
                                print(f"    • ✅ Safety Words: {jp_analysis['safety_words']}")
                            else:
                                print(f"    • ❌ No Japanese characters detected!")
                            
                            print(f"  🎯 Cultural Score: {result['cultural_score']:.1f}/10")
                            
                            # Save sample
                            sample_filename = f"japan_{occasion}_{tone}_{product_config['name'].replace(' ', '_')}.json"
                            with open(sample_filename, 'w', encoding='utf-8') as f:
                                json.dump({
                                    'title': title,
                                    'bullets': bullets,
                                    'description': description[:500],
                                    'analysis': jp_analysis
                                }, f, indent=2, ensure_ascii=False)
                            
                            overall_results.append(result)
                            
                        else:
                            print(f"  ❌ No listing generated")
                            
                    except Exception as e:
                        print(f"  ❌ Error: {str(e)[:100]}")
                        
                    finally:
                        product.delete()
        
        # Final Analysis
        self.print_final_analysis(overall_results)
        return overall_results
    
    def calculate_cultural_score(self, analysis):
        """Calculate cultural adaptation score for Japan market"""
        score = 0
        
        # Japanese characters (4 points)
        if analysis['has_japanese']:
            score += 4
            if len(analysis['character_types']) >= 2:  # Multiple character types
                score += 1
        
        # Politeness level (2 points)
        score += min(2, analysis['politeness_level'] * 0.5)
        
        # Quality emphasis (2 points)
        score += min(2, analysis['quality_words'] * 0.5)
        
        # Respect for customers (1 point)
        if analysis['respect_words'] > 0:
            score += 1
        
        # Safety emphasis (1 point) - very important in Japan
        if analysis['safety_words'] > 0:
            score += 1
        
        return min(10, score)
    
    def print_final_analysis(self, results):
        """Print comprehensive final analysis"""
        print("\n\n" + "="*80)
        print("🇯🇵 JAPAN MARKET FINAL ANALYSIS")
        print("="*80)
        
        if not results:
            print("❌ No results to analyze")
            return
        
        # Calculate averages
        avg_cultural_score = sum(r['cultural_score'] for r in results) / len(results)
        japanese_success_rate = sum(1 for r in results if r['has_proper_encoding']) / len(results) * 100
        
        print(f"\n📊 Overall Performance:")
        print(f"  • Average Cultural Score: {avg_cultural_score:.1f}/10")
        print(f"  • Japanese Encoding Success: {japanese_success_rate:.1f}%")
        print(f"  • Total Tests Completed: {len(results)}")
        
        # Best performing combinations
        best_results = sorted(results, key=lambda x: x['cultural_score'], reverse=True)[:5]
        print(f"\n🏆 Top 5 Cultural Adaptations:")
        for i, result in enumerate(best_results, 1):
            print(f"  {i}. {result['product']} ({result['occasion']} + {result['tone']}) - {result['cultural_score']:.1f}/10")
        
        # Category analysis
        print(f"\n📈 Performance by Occasion:")
        occasion_scores = {}
        for result in results:
            occasion = result['occasion']
            if occasion not in occasion_scores:
                occasion_scores[occasion] = []
            occasion_scores[occasion].append(result['cultural_score'])
        
        for occasion, scores in occasion_scores.items():
            avg_score = sum(scores) / len(scores)
            print(f"  • {occasion}: {avg_score:.1f}/10 ({len(scores)} tests)")
        
        # Recommendations
        print(f"\n💡 Recommendations:")
        if avg_cultural_score >= 8:
            print("  ✅ EXCELLENT: Japan market ready for production!")
        elif avg_cultural_score >= 6:
            print("  ⚠️  GOOD: Minor improvements needed for optimal performance")
            print("    - Increase use of Japanese politeness markers")
            print("    - Add more quality/safety emphasis")
        else:
            print("  ❌ NEEDS WORK: Significant improvements required")
            print("    - Ensure proper Japanese character encoding")
            print("    - Implement cultural politeness standards")
            print("    - Add quality and safety emphasis")
        
        print(f"\n🌸 Cultural Notes for Japan Market:")
        print("  • Quality and safety are paramount concerns")
        print("  • Politeness and respect for customers is essential")
        print("  • Gift-giving occasions (お中元, お歳暮) are very important")
        print("  • Detailed specifications and certifications build trust")

if __name__ == "__main__":
    tester = JapanMarketTester()
    results = tester.test_japan_market()
    
    # Save comprehensive results
    with open('japan_market_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    
    print("\n\n✅ Japan market testing complete!")
    print("📁 Detailed results saved to japan_market_results.json")
    print("📁 Individual samples saved as japan_*.json files")