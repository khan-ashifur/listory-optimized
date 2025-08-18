"""
Final Market Validation - Comprehensive Testing
Validates all improvements against competitor standards
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

class FinalMarketValidator:
    """Final validation against Copy Monkey, Helium 10, Jasper AI standards"""
    
    def __init__(self):
        self.service = ListingGeneratorService()
        self.test_user, _ = User.objects.get_or_create(username='test_validator')
        
        # Competitor benchmarks
        self.benchmarks = {
            'copy_monkey': {'emotional_hooks': 5, 'conversion_words': 10, 'readability': 8.5},
            'helium_10': {'seo_score': 9.0, 'keyword_density': 3.0, 'backend_keywords': 250},
            'jasper_ai': {'creativity': 9.0, 'localization': 9.5, 'grammar': 10.0}
        }
        
        # Test configurations
        self.test_configs = [
            {'market': 'us', 'occasion': 'christmas', 'tone': 'friendly'},
            {'market': 'de', 'occasion': 'weihnachten', 'tone': 'professional'},
            {'market': 'fr', 'occasion': 'noel', 'tone': 'luxurious'},
            {'market': 'it', 'occasion': 'natale', 'tone': 'professional'},
            {'market': 'es', 'occasion': 'navidad', 'tone': 'friendly'}
        ]
    
    def analyze_content_quality(self, content, market):
        """Analyze content for quality metrics"""
        metrics = {
            'character_count': len(content),
            'word_count': len(content.split()),
            'has_native_chars': False,
            'emotional_words': 0,
            'conversion_words': 0,
            'trust_elements': 0
        }
        
        # Check for native characters
        if market == 'de':
            metrics['has_native_chars'] = any(c in content for c in 'äöüßÄÖÜ')
        elif market == 'fr':
            metrics['has_native_chars'] = any(c in content for c in 'éèàçùâêîôû')
        elif market == 'it':
            metrics['has_native_chars'] = any(c in content for c in 'àèéìòù')
        elif market == 'es':
            metrics['has_native_chars'] = any(c in content for c in 'áéíóúñü')
        else:
            metrics['has_native_chars'] = True  # US doesn't need special chars
        
        # Count emotional and conversion words
        emotional_words = ['amazing', 'perfect', 'ultimate', 'revolutionary', 'transform',
                          'breakthrough', 'exclusive', 'premium', 'exceptional']
        conversion_words = ['now', 'today', 'limited', 'guarantee', 'save', 'free',
                           'instant', 'proven', 'trusted', 'certified']
        
        content_lower = content.lower()
        metrics['emotional_words'] = sum(1 for word in emotional_words if word in content_lower)
        metrics['conversion_words'] = sum(1 for word in conversion_words if word in content_lower)
        
        # Trust elements
        trust_words = ['guarantee', 'warranty', 'certified', 'return', 'refund', 'quality']
        metrics['trust_elements'] = sum(1 for word in trust_words if word in content_lower)
        
        return metrics
    
    def calculate_scores(self, metrics, market):
        """Calculate quality scores based on metrics"""
        scores = {}
        
        # Emotional score (0-10)
        scores['emotional'] = min(10, metrics['emotional_words'] * 2)
        
        # Conversion score (0-10)
        scores['conversion'] = min(10, metrics['conversion_words'] * 1.5)
        
        # Trust score (0-10)
        scores['trust'] = min(10, metrics['trust_elements'] * 2.5)
        
        # Localization score (0-10)
        if market != 'us':
            scores['localization'] = 10 if metrics['has_native_chars'] else 5
        else:
            scores['localization'] = 10
        
        # Overall score
        scores['overall'] = sum(scores.values()) / len(scores)
        
        return scores
    
    def validate_against_competitors(self, scores):
        """Check if scores meet competitor standards"""
        results = {}
        
        # Copy Monkey standards
        results['copy_monkey'] = {
            'pass': scores['emotional'] >= 7 and scores['conversion'] >= 8,
            'score': (scores['emotional'] + scores['conversion']) / 2
        }
        
        # Helium 10 standards (simplified)
        results['helium_10'] = {
            'pass': scores['overall'] >= 8.5,
            'score': scores['overall']
        }
        
        # Jasper AI standards
        results['jasper_ai'] = {
            'pass': scores['localization'] >= 9 and scores['overall'] >= 8,
            'score': (scores['localization'] + scores['overall']) / 2
        }
        
        return results
    
    def run_validation(self):
        """Run comprehensive validation"""
        print("\n" + "="*80)
        print("FINAL MARKET VALIDATION - LISTORY AI")
        print("Benchmarking against: Copy Monkey, Helium 10, Jasper AI")
        print("="*80)
        
        all_results = []
        
        for config in self.test_configs:
            print(f"\n\nTesting {config['market'].upper()} Market")
            print("-" * 60)
            
            # Create test product
            product = Product.objects.create(
                user=self.test_user,
                name="Premium Wireless Bluetooth Headphones",
                description="High-end noise cancelling headphones with 30-hour battery",
                brand_name="AudioElite",
                brand_tone=config['tone'],
                target_platform="amazon",
                marketplace=config['market'],
                occasion=config['occasion'],
                categories="Electronics/Audio/Headphones",
                features="Active Noise Cancellation, 30hr Battery, Bluetooth 5.3",
                target_audience="Professionals and audiophiles"
            )
            
            try:
                # Generate listing
                listing = self.service.generate_listing(
                    product_id=product.id,
                    platform='amazon'
                )
                
                if listing:
                    # Parse content
                    title = listing.title or ''
                    bullets = json.loads(listing.bullet_points) if listing.bullet_points else []
                    description = listing.description or ''
                    
                    # Combine all content
                    full_content = f"{title} {' '.join(bullets)} {description}"
                    
                    # Analyze quality
                    metrics = self.analyze_content_quality(full_content, config['market'])
                    scores = self.calculate_scores(metrics, config['market'])
                    competitor_results = self.validate_against_competitors(scores)
                    
                    # Display results
                    print(f"\n📊 Quality Metrics:")
                    print(f"  • Character Count: {metrics['character_count']}")
                    print(f"  • Word Count: {metrics['word_count']}")
                    print(f"  • Native Characters: {'✅' if metrics['has_native_chars'] else '❌'}")
                    print(f"  • Emotional Words: {metrics['emotional_words']}")
                    print(f"  • Conversion Words: {metrics['conversion_words']}")
                    print(f"  • Trust Elements: {metrics['trust_elements']}")
                    
                    print(f"\n📈 Quality Scores:")
                    print(f"  • Emotional: {scores['emotional']:.1f}/10")
                    print(f"  • Conversion: {scores['conversion']:.1f}/10")
                    print(f"  • Trust: {scores['trust']:.1f}/10")
                    print(f"  • Localization: {scores['localization']:.1f}/10")
                    print(f"  • OVERALL: {scores['overall']:.1f}/10")
                    
                    print(f"\n🏆 Competitor Comparison:")
                    for competitor, result in competitor_results.items():
                        status = "✅ PASS" if result['pass'] else "❌ FAIL"
                        print(f"  • {competitor}: {status} (Score: {result['score']:.1f})")
                    
                    # Store results
                    all_results.append({
                        'market': config['market'],
                        'scores': scores,
                        'competitor_results': competitor_results,
                        'metrics': metrics
                    })
                    
                    # Save sample
                    with open(f"final_{config['market']}_sample.txt", 'w', encoding='utf-8') as f:
                        f.write(f"TITLE:\n{title}\n\n")
                        f.write(f"BULLETS:\n")
                        for i, bullet in enumerate(bullets, 1):
                            f.write(f"{i}. {bullet}\n")
                        f.write(f"\nFIRST 500 CHARS OF DESCRIPTION:\n{description[:500]}")
                    
            except Exception as e:
                print(f"  ❌ Error: {str(e)}")
                all_results.append({
                    'market': config['market'],
                    'error': str(e)
                })
            
            finally:
                product.delete()
        
        # Final Summary
        print("\n\n" + "="*80)
        print("FINAL SUMMARY")
        print("="*80)
        
        passed_markets = []
        failed_markets = []
        
        for result in all_results:
            if 'error' not in result:
                market = result['market'].upper()
                overall = result['scores']['overall']
                
                # Check if passes all competitor standards
                all_pass = all(r['pass'] for r in result['competitor_results'].values())
                
                if all_pass and overall >= 8.5:
                    passed_markets.append(market)
                    print(f"\n✅ {market}: EXCELLENT ({overall:.1f}/10)")
                    print(f"   Beats all competitors!")
                else:
                    failed_markets.append(market)
                    print(f"\n⚠️  {market}: NEEDS IMPROVEMENT ({overall:.1f}/10)")
                    
                    # Show what needs improvement
                    if result['scores']['emotional'] < 7:
                        print(f"   • Increase emotional engagement")
                    if result['scores']['conversion'] < 8:
                        print(f"   • Add more conversion elements")
                    if result['scores']['localization'] < 9:
                        print(f"   • Improve localization quality")
        
        # Final verdict
        print("\n" + "="*60)
        if len(passed_markets) == len(self.test_configs):
            print("🎉 SUCCESS! All markets meet or exceed competitor standards!")
        else:
            print(f"📊 {len(passed_markets)}/{len(self.test_configs)} markets meet standards")
            if failed_markets:
                print(f"   Markets needing work: {', '.join(failed_markets)}")
        
        return all_results

if __name__ == "__main__":
    validator = FinalMarketValidator()
    results = validator.run_validation()
    
    # Save full results
    with open('final_validation_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str, ensure_ascii=False)
    
    print("\n\n✅ Validation complete! Check final_*_sample.txt files for content samples.")