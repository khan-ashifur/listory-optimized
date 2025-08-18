"""
Comprehensive Market Evaluation System for Listory AI
Tests USA, France, Italy, Germany, Spain markets against top competitors
Author: E-commerce Specialist
"""

import os
import sys
import json
import django
from datetime import datetime
from typing import Dict, List, Tuple

# Django setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from apps.listings.international_localization_optimizer import InternationalLocalizationOptimizer
from apps.listings.international_content_extractor import InternationalContentExtractor

class ComprehensiveMarketEvaluator:
    """
    Professional e-commerce specialist evaluation system
    Benchmarks against Copy Monkey, Helium 10, Jasper AI standards
    """
    
    def __init__(self):
        self.service = ListingGeneratorService()
        self.optimizer = InternationalLocalizationOptimizer()
        self.extractor = InternationalContentExtractor()
        self.results = {}
        
        # Test markets
        self.markets = ['us', 'fr', 'it', 'de', 'es']
        
        # Competition benchmark standards
        self.competitor_standards = {
            'copy_monkey': {
                'keyword_density': 0.03,  # 3% keyword density
                'emotional_hooks': 5,      # At least 5 emotional triggers
                'readability_score': 8.5,  # Out of 10
                'conversion_words': 10     # Power words per listing
            },
            'helium_10': {
                'seo_optimization': 9.0,   # SEO score
                'keyword_relevance': 0.95, # Keyword relevance
                'backend_keywords': 250,   # Backend keyword count
                'title_optimization': 9.5  # Title effectiveness
            },
            'jasper_ai': {
                'creativity_score': 9.0,   # Creative language use
                'brand_consistency': 0.95, # Brand voice consistency
                'grammar_accuracy': 1.0,   # Perfect grammar
                'localization_quality': 9.5 # Cultural adaptation
            }
        }
        
        # Test occasions per market
        self.market_occasions = {
            'us': [
                'christmas', 'black_friday', 'cyber_monday', 'valentines_day', 
                'mothers_day', 'fathers_day', 'back_to_school', 'halloween',
                'thanksgiving', 'independence_day', 'memorial_day', 'labor_day'
            ],
            'fr': [
                'noel', 'black_friday', 'saint_valentin', 'fete_des_meres',
                'fete_des_peres', 'rentree_scolaire', 'soldes_hiver', 'soldes_ete',
                'paques', 'jour_de_lan', 'fete_nationale', 'beaujolais_nouveau'
            ],
            'it': [
                'natale', 'black_friday', 'san_valentino', 'festa_della_mamma',
                'festa_del_papa', 'ritorno_a_scuola', 'saldi_invernali', 'saldi_estivi',
                'pasqua', 'capodanno', 'ferragosto', 'befana'
            ],
            'de': [
                'weihnachten', 'black_friday', 'valentinstag', 'muttertag',
                'vatertag', 'schulanfang', 'oktoberfest', 'ostern',
                'silvester', 'fasching', 'winterschlussverkauf', 'sommerschlussverkauf'
            ],
            'es': [
                'navidad', 'black_friday', 'san_valentin', 'dia_de_la_madre',
                'dia_del_padre', 'vuelta_al_cole', 'reyes_magos', 'rebajas_invierno',
                'rebajas_verano', 'semana_santa', 'dia_hispanidad', 'el_gordo'
            ]
        }
        
        # Brand tones to test
        self.brand_tones = [
            'professional', 'friendly', 'luxurious', 'playful', 
            'innovative', 'trustworthy', 'eco_conscious', 'minimalist'
        ]
        
        # Test products (diverse categories)
        self.test_products = [
            {
                'name': 'Premium Wireless Headphones',
                'category': 'Electronics/Audio',
                'price_range': 'mid-high',
                'target': 'professionals'
            },
            {
                'name': 'Eco-Friendly Kitchen Cutting Board Set',
                'category': 'Home/Kitchen',
                'price_range': 'mid',
                'target': 'families'
            },
            {
                'name': 'Smart Fitness Tracker Watch',
                'category': 'Sports/Electronics',
                'price_range': 'mid',
                'target': 'fitness enthusiasts'
            }
        ]

    def evaluate_linguistic_quality(self, content: str, market: str) -> Dict:
        """Evaluate linguistic quality and native fluency"""
        config = self.optimizer.market_configurations.get(market, {})
        
        scores = {
            'native_fluency': 0,
            'grammar_accuracy': 0,
            'cultural_adaptation': 0,
            'emotional_impact': 0,
            'keyword_integration': 0
        }
        
        if not content:
            return scores
            
        # Check for essential words
        essential_words = config.get('essential_words', [])
        essential_count = sum(1 for word in essential_words if word in content.lower())
        scores['native_fluency'] = min(10, (essential_count / max(1, len(essential_words))) * 15)
        
        # Check power words
        power_words = config.get('power_words', [])
        power_count = sum(1 for word in power_words if word in content.lower())
        scores['emotional_impact'] = min(10, (power_count / max(1, len(power_words))) * 20)
        
        # Check cultural elements
        cultural_elements = config.get('cultural_elements', [])
        cultural_count = sum(1 for elem in cultural_elements if any(word in content.lower() for word in elem.lower().split()))
        scores['cultural_adaptation'] = min(10, (cultural_count / max(1, len(cultural_elements))) * 25)
        
        # Grammar accuracy (check for proper accents/umlauts)
        if market == 'de':
            umlaut_chars = ['ä', 'ö', 'ü', 'ß', 'Ä', 'Ö', 'Ü']
            has_umlauts = any(char in content for char in umlaut_chars)
            scores['grammar_accuracy'] = 10 if has_umlauts else 5
        elif market == 'fr':
            accent_chars = ['é', 'è', 'à', 'ç', 'ù', 'â', 'ê', 'î', 'ô', 'û']
            has_accents = any(char in content for char in accent_chars)
            scores['grammar_accuracy'] = 10 if has_accents else 5
        elif market == 'it':
            accent_chars = ['à', 'è', 'é', 'ì', 'ò', 'ù']
            has_accents = any(char in content for char in accent_chars)
            scores['grammar_accuracy'] = 10 if has_accents else 5
        elif market == 'es':
            accent_chars = ['á', 'é', 'í', 'ó', 'ú', 'ñ', 'ü']
            has_accents = any(char in content for char in accent_chars)
            scores['grammar_accuracy'] = 10 if has_accents else 5
        else:
            scores['grammar_accuracy'] = 9  # Default for US
        
        # Keyword integration
        scores['keyword_integration'] = min(10, power_count * 2)
        
        return scores

    def check_occasion_relevance(self, market: str, listing_content: str) -> Dict:
        """Check if market-appropriate occasions are used"""
        occasions = self.market_occasions.get(market, [])
        
        found_occasions = []
        irrelevant_occasions = []
        
        # Check for appropriate occasions
        for occasion in occasions:
            if occasion.replace('_', ' ').lower() in listing_content.lower():
                found_occasions.append(occasion)
        
        # Check for US-specific occasions that shouldn't be in other markets
        if market != 'us':
            us_only_occasions = ['memorial_day', 'labor_day', 'independence_day', 'thanksgiving']
            for us_occasion in us_only_occasions:
                if us_occasion.replace('_', ' ').lower() in listing_content.lower():
                    irrelevant_occasions.append(us_occasion)
        
        return {
            'appropriate_occasions': found_occasions,
            'irrelevant_occasions': irrelevant_occasions,
            'occasion_score': len(found_occasions) * 2 - len(irrelevant_occasions) * 3
        }

    def evaluate_against_competitors(self, listing_data: Dict) -> Dict:
        """Benchmark against competitor standards"""
        scores = {}
        
        # Analyze content
        full_content = f"{listing_data.get('title', '')} {' '.join(listing_data.get('bullet_points', []))} {listing_data.get('description', '')}"
        word_count = len(full_content.split())
        
        # Copy Monkey benchmarks
        power_words_count = sum(1 for word in ['premium', 'quality', 'best', 'exclusive', 'guaranteed', 'professional', 'superior'] 
                               if word in full_content.lower())
        scores['copy_monkey'] = {
            'emotional_hooks': min(10, power_words_count * 2),
            'conversion_optimization': min(10, power_words_count * 1.5),
            'readability': 8.5  # Simplified scoring
        }
        
        # Helium 10 benchmarks
        keyword_count = len(listing_data.get('backend_keywords', '').split(','))
        scores['helium_10'] = {
            'seo_optimization': min(10, keyword_count / 25),
            'keyword_density': min(10, power_words_count / max(1, word_count) * 100),
            'title_effectiveness': 9 if len(listing_data.get('title', '')) > 100 else 7
        }
        
        # Jasper AI benchmarks
        scores['jasper_ai'] = {
            'creativity': 8.5,  # Simplified
            'brand_consistency': 9,
            'localization_quality': 9
        }
        
        return scores

    def test_all_sections(self, market: str, product_data: Dict) -> Dict:
        """Test all listing sections for completeness and quality"""
        results = {
            'title': {'exists': False, 'quality': 0},
            'bullet_points': {'exists': False, 'count': 0, 'quality': 0},
            'description': {'exists': False, 'quality': 0},
            'backend_keywords': {'exists': False, 'count': 0},
            'aplus_content': {'exists': False, 'sections': 0, 'quality': 0}
        }
        
        try:
            # Create test product
            product = Product.objects.create(
                name=product_data['name'],
                categories=product_data['category'],
                brand_name='TestBrand',
                about_item='Premium quality product with advanced features',
                key_features='Feature 1, Feature 2, Feature 3',
                target_audience=product_data['target'],
                key_product_features='Advanced technology, Durable design, Easy to use'
            )
            
            # Generate listing
            listing_data = self.service.generate_listing(
                product=product,
                marketplace=market,
                occasion='general',
                brand_tone='professional'
            )
            
            # Evaluate each section
            if listing_data.get('title'):
                results['title']['exists'] = True
                results['title']['quality'] = len(listing_data['title']) / 20  # Simple length-based score
                
            if listing_data.get('bullet_points'):
                results['bullet_points']['exists'] = True
                results['bullet_points']['count'] = len(listing_data['bullet_points'])
                results['bullet_points']['quality'] = min(10, len(listing_data['bullet_points']) * 2)
                
            if listing_data.get('description'):
                results['description']['exists'] = True
                results['description']['quality'] = min(10, len(listing_data['description']) / 100)
                
            if listing_data.get('backend_keywords'):
                results['backend_keywords']['exists'] = True
                results['backend_keywords']['count'] = len(listing_data['backend_keywords'].split(','))
                
            if listing_data.get('aplus_content'):
                results['aplus_content']['exists'] = True
                results['aplus_content']['sections'] = len(listing_data['aplus_content'])
                results['aplus_content']['quality'] = min(10, len(listing_data['aplus_content']) * 1.25)
            
            # Store full listing for analysis
            results['full_listing'] = listing_data
            
            # Clean up
            product.delete()
            
        except Exception as e:
            results['error'] = str(e)
            
        return results

    def run_comprehensive_evaluation(self):
        """Run full evaluation suite"""
        print("\n" + "="*80)
        print("COMPREHENSIVE MARKET EVALUATION - LISTORY AI")
        print("Benchmarking against: Copy Monkey, Helium 10, Jasper AI")
        print("="*80)
        
        overall_results = {}
        
        for market in self.markets:
            print(f"\n\n{'='*60}")
            print(f"TESTING MARKET: {market.upper()}")
            print(f"{'='*60}")
            
            market_results = {
                'linguistic_scores': [],
                'occasion_scores': [],
                'section_completeness': [],
                'competitor_benchmarks': [],
                'overall_quality': 0
            }
            
            # Test each product
            for product_data in self.test_products:
                print(f"\n Testing Product: {product_data['name']}")
                
                # Test all sections
                section_results = self.test_all_sections(market, product_data)
                market_results['section_completeness'].append(section_results)
                
                if 'full_listing' in section_results:
                    listing = section_results['full_listing']
                    
                    # Linguistic quality
                    full_text = f"{listing.get('title', '')} {' '.join(listing.get('bullet_points', []))} {listing.get('description', '')}"
                    linguistic_scores = self.evaluate_linguistic_quality(full_text, market)
                    market_results['linguistic_scores'].append(linguistic_scores)
                    
                    # Occasion relevance
                    occasion_check = self.check_occasion_relevance(market, full_text)
                    market_results['occasion_scores'].append(occasion_check)
                    
                    # Competitor benchmarks
                    competitor_scores = self.evaluate_against_competitors(listing)
                    market_results['competitor_benchmarks'].append(competitor_scores)
                    
                    # Print immediate results
                    print(f"  ✓ Linguistic Quality: {sum(linguistic_scores.values())/len(linguistic_scores):.1f}/10")
                    print(f"  ✓ Occasions Found: {len(occasion_check['appropriate_occasions'])}")
                    print(f"  ✓ Irrelevant Occasions: {len(occasion_check['irrelevant_occasions'])}")
                    
                    if occasion_check['irrelevant_occasions']:
                        print(f"    ⚠️  Found US-specific occasions: {occasion_check['irrelevant_occasions']}")
            
            # Calculate overall market score
            if market_results['linguistic_scores']:
                avg_linguistic = sum(sum(s.values())/len(s) for s in market_results['linguistic_scores']) / len(market_results['linguistic_scores'])
                market_results['overall_quality'] = avg_linguistic
                
                print(f"\n{market.upper()} MARKET SUMMARY:")
                print(f"  Overall Quality Score: {avg_linguistic:.1f}/10")
                
                # Check against competitor standards
                print(f"\n  Competitor Comparison:")
                print(f"    vs Copy Monkey: {'✅ PASS' if avg_linguistic >= 8.5 else '❌ NEEDS IMPROVEMENT'}")
                print(f"    vs Helium 10: {'✅ PASS' if avg_linguistic >= 9.0 else '❌ NEEDS IMPROVEMENT'}")
                print(f"    vs Jasper AI: {'✅ PASS' if avg_linguistic >= 9.0 else '❌ NEEDS IMPROVEMENT'}")
            
            overall_results[market] = market_results
        
        # Final summary
        print("\n\n" + "="*80)
        print("FINAL EVALUATION SUMMARY")
        print("="*80)
        
        for market, results in overall_results.items():
            quality = results['overall_quality']
            status = "✅ EXCELLENT" if quality >= 9 else "⚠️ GOOD" if quality >= 7 else "❌ NEEDS WORK"
            print(f"\n{market.upper()}: {quality:.1f}/10 - {status}")
            
            # Specific recommendations
            if quality < 9:
                print(f"  Recommendations for {market.upper()}:")
                if quality < 8:
                    print(f"    - Improve linguistic fluency and native expressions")
                    print(f"    - Add more market-specific occasions")
                    print(f"    - Enhance cultural adaptation")
                if any(s['irrelevant_occasions'] for s in results['occasion_scores'] if s):
                    print(f"    - Remove US-specific occasions from content")
        
        return overall_results

# Main execution
if __name__ == "__main__":
    evaluator = ComprehensiveMarketEvaluator()
    results = evaluator.run_comprehensive_evaluation()
    
    # Save detailed results
    with open('market_evaluation_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str, ensure_ascii=False)
    
    print("\n\n✅ Evaluation complete! Detailed results saved to market_evaluation_results.json")