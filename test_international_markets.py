"""
Comprehensive International Marketplace Testing System
Tests all major Amazon markets with proper language localization
Evaluates cultural adaptation and localization quality to achieve 10/10
"""

import os
import sys
import django
import json
import time
from datetime import datetime

# Add the backend directory to the Python path
sys.path.insert(0, r'C:\Users\khana\Desktop\listory-ai\backend')

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "listory.settings")
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from apps.listings.models import GeneratedListing

class InternationalMarketTester:
    def __init__(self):
        self.service = ListingGeneratorService()
        # Major Amazon international markets
        self.markets = {
            'de': {
                'name': 'Germany', 
                'marketplace': 'de',
                'language': 'de',
                'currency': 'EUR',
                'expected_language': 'German',
                'sample_words': ['der', 'die', 'das', 'und', 'mit', 'für', 'von', 'zu', 'ist', 'haben'],
                'cultural_elements': ['qualität', 'zuverlässig', 'präzision', 'funktional', 'hochwertig'],
                'avoid_words': ['the', 'and', 'with', 'for', 'is']
            },
            'fr': {
                'name': 'France',
                'marketplace': 'fr', 
                'language': 'fr',
                'currency': 'EUR',
                'expected_language': 'French',
                'sample_words': ['le', 'la', 'les', 'et', 'avec', 'pour', 'de', 'du', 'est', 'avoir'],
                'cultural_elements': ['qualité', 'élégant', 'raffinement', 'sophistiqué', 'excellence'],
                'avoid_words': ['the', 'and', 'with', 'for', 'is']
            },
            'it': {
                'name': 'Italy',
                'marketplace': 'it',
                'language': 'it', 
                'currency': 'EUR',
                'expected_language': 'Italian',
                'sample_words': ['il', 'la', 'le', 'e', 'con', 'per', 'di', 'da', 'è', 'avere'],
                'cultural_elements': ['qualità', 'eleganza', 'stile', 'raffinato', 'bellezza'],
                'avoid_words': ['the', 'and', 'with', 'for', 'is']
            },
            'es': {
                'name': 'Spain',
                'marketplace': 'es',
                'language': 'es',
                'currency': 'EUR', 
                'expected_language': 'Spanish',
                'sample_words': ['el', 'la', 'los', 'y', 'con', 'para', 'de', 'del', 'es', 'tener'],
                'cultural_elements': ['calidad', 'excelente', 'funcional', 'práctico', 'innovador'],
                'avoid_words': ['the', 'and', 'with', 'for', 'is']
            },
            'ar': {
                'name': 'Saudi Arabia/UAE',
                'marketplace': 'ae',
                'language': 'ar',
                'currency': 'AED',
                'expected_language': 'Arabic',
                'sample_words': ['في', 'من', 'إلى', 'على', 'عن', 'مع', 'هو', 'هي', 'كان', 'يكون'],
                'cultural_elements': ['جودة عالية', 'ممتاز', 'موثوق', 'عملي', 'متطور'],
                'avoid_words': ['the', 'and', 'with', 'for', 'is'],
                'rtl': True
            },
            'nl': {
                'name': 'Netherlands',
                'marketplace': 'nl',
                'language': 'nl',
                'currency': 'EUR',
                'expected_language': 'Dutch', 
                'sample_words': ['de', 'het', 'een', 'en', 'met', 'voor', 'van', 'te', 'is', 'hebben'],
                'cultural_elements': ['kwaliteit', 'praktisch', 'betrouwbaar', 'functioneel', 'doeltreffend'],
                'avoid_words': ['the', 'and', 'with', 'for', 'is']
            },
            'ja': {
                'name': 'Japan',
                'marketplace': 'co.jp',
                'language': 'ja',
                'currency': 'JPY',
                'expected_language': 'Japanese',
                'sample_words': ['の', 'に', 'を', 'は', 'が', 'と', 'で', 'から', 'まで', 'より'],
                'cultural_elements': ['品質', '信頼性', '機能的', '高品質', '優れた'],
                'avoid_words': ['the', 'and', 'with', 'for', 'is'],
                'special_chars': True
            }
        }
        self.results = {}
        
    def evaluate_language_quality(self, listing, market_config):
        """Comprehensive evaluation of language localization quality"""
        
        market_name = market_config['name']
        expected_lang = market_config['expected_language']
        
        if not listing or listing.status != 'completed':
            return {
                'overall_score': 0,
                'language_score': 0,
                'cultural_score': 0,
                'localization_score': 0,
                'issues': ['Listing generation failed']
            }
        
        analysis = {
            'language_score': 0,
            'cultural_score': 0, 
            'localization_score': 0,
            'issues': []
        }
        
        # Combine all text for analysis
        all_text = ' '.join([
            listing.title or '',
            listing.bullet_points or '',
            listing.long_description or ''
        ])
        
        if not all_text.strip():
            analysis['issues'].append("❌ No content generated")
            return analysis
        
        all_text_lower = all_text.lower()
        
        # === LANGUAGE ACCURACY ANALYSIS ===
        
        # Check for proper language usage
        native_words_found = sum(1 for word in market_config['sample_words'] if word in all_text_lower)
        if native_words_found >= 5:
            analysis['language_score'] += 40
        elif native_words_found >= 3:
            analysis['language_score'] += 25
        elif native_words_found >= 1:
            analysis['language_score'] += 10
        else:
            analysis['issues'].append(f"❌ Missing {expected_lang} language indicators")
        
        # Check for English contamination (should be avoided)
        english_contamination = sum(1 for word in market_config['avoid_words'] if word in all_text_lower)
        if english_contamination == 0:
            analysis['language_score'] += 40
        elif english_contamination <= 2:
            analysis['language_score'] += 20
        else:
            analysis['issues'].append(f"❌ Contains {english_contamination} English words (should be 0)")
        
        # Check for proper character encoding (especially for Arabic/Japanese)
        if market_config.get('special_chars') or market_config.get('rtl'):
            # Check for proper Unicode handling
            try:
                all_text.encode('utf-8')
                analysis['language_score'] += 20
            except UnicodeEncodeError:
                analysis['issues'].append("❌ Character encoding issues")
        else:
            analysis['language_score'] += 20
        
        # === CULTURAL ADAPTATION ANALYSIS ===
        
        # Check for cultural elements
        cultural_elements_found = sum(1 for element in market_config['cultural_elements'] if element in all_text_lower)
        if cultural_elements_found >= 3:
            analysis['cultural_score'] += 50
        elif cultural_elements_found >= 2:
            analysis['cultural_score'] += 30
        elif cultural_elements_found >= 1:
            analysis['cultural_score'] += 15
        else:
            analysis['issues'].append(f"❌ Missing cultural elements for {market_name}")
        
        # Check for appropriate formality level
        # Different markets have different formality expectations
        formality_indicators = {
            'de': ['sie', 'ihr', 'hochwertigen', 'professionell'],  # German formal
            'fr': ['vous', 'votre', 'excellence', 'raffinement'],   # French formal  
            'ja': ['です', 'ます', '致します', 'ございます'],           # Japanese formal
            'ar': ['حضرتكم', 'سيادتكم', 'المحترم'],                # Arabic formal
            'it': ['lei', 'suo', 'professionale', 'eccellenza'],    # Italian formal
            'es': ['usted', 'su', 'excelente', 'profesional'],     # Spanish formal
            'nl': ['u', 'uw', 'professioneel', 'kwaliteit']        # Dutch formal
        }
        
        lang = market_config['language']
        if lang in formality_indicators:
            formality_found = sum(1 for indicator in formality_indicators[lang] if indicator in all_text_lower)
            if formality_found >= 1:
                analysis['cultural_score'] += 50
            else:
                analysis['issues'].append(f"⚠️ Consider adding formal language for {market_name}")
        
        # === LOCALIZATION QUALITY ANALYSIS ===
        
        # Check for proper product naming conventions
        if listing.title:
            title = listing.title
            # Check title length appropriate for market
            if 50 <= len(title) <= 200:
                analysis['localization_score'] += 25
            else:
                analysis['issues'].append(f"⚠️ Title length: {len(title)} chars (optimal: 50-200 for {market_name})")
        
        # Check for market-appropriate keywords
        if listing.keywords:
            keywords_text = listing.keywords.lower() if listing.keywords else ''
            market_keywords = sum(1 for word in market_config['sample_words'] if word in keywords_text)
            if market_keywords >= 3:
                analysis['localization_score'] += 25
            else:
                analysis['issues'].append(f"⚠️ Keywords need more {expected_lang} terms")
        
        # Check for proper bullet point structure
        if listing.bullet_points:
            bullets = listing.bullet_points.split('\n')
            if len(bullets) >= 3:
                analysis['localization_score'] += 25
            
            # Check bullets contain native language
            bullets_text = listing.bullet_points.lower()
            bullet_lang_score = sum(1 for word in market_config['sample_words'] if word in bullets_text)
            if bullet_lang_score >= 3:
                analysis['localization_score'] += 25
            else:
                analysis['issues'].append(f"⚠️ Bullets need more {expected_lang} content")
        
        # Calculate overall score
        analysis['overall_score'] = (
            analysis['language_score'] + 
            analysis['cultural_score'] + 
            analysis['localization_score']
        ) / 3
        
        return analysis
    
    def test_market(self, market_code):
        """Test a single international market comprehensively"""
        
        if market_code not in self.markets:
            print(f"❌ Unknown market: {market_code}")
            return None
            
        market_config = self.markets[market_code]
        market_name = market_config['name']
        
        print(f"\n{'='*80}")
        print(f"🌍 TESTING MARKET: {market_name.upper()} ({market_code.upper()})")
        print(f"{'='*80}")
        
        print(f"Market: Amazon.{market_config['marketplace']}")
        print(f"Language: {market_config['expected_language']} ({market_code})")
        print(f"Currency: {market_config['currency']}")
        print(f"Expected Elements: {', '.join(market_config['cultural_elements'][:3])}")
        
        try:
            # Find test product
            product = Product.objects.filter(name__icontains="misting fan").first()
            if not product:
                print("❌ No test product found")
                return None
                
            # Set market and language
            product.marketplace = market_config['marketplace']
            product.marketplace_language = market_config['language'] 
            product.brand_tone = 'professional'  # Test professional tone
            product.occasion = 'None'  # Test general listing first
            product.save()
            
            print(f"\nProduct: {product.name}")
            print(f"Set to: Amazon.{product.marketplace} ({product.marketplace_language})")
            print("Generating localized listing...")
            
            # Generate listing
            self.service.generate_listing(product.id, 'amazon')
            
            # Wait for generation
            time.sleep(8)  # Longer wait for international generation
            
            # Get the listing
            listing = GeneratedListing.objects.filter(
                product=product,
                platform='amazon'
            ).order_by('-created_at').first()
            
            if listing and listing.status == 'completed':
                # Evaluate localization quality
                analysis = self.evaluate_language_quality(listing, market_config)
                
                # Display results
                print(f"\n📊 LOCALIZATION QUALITY ANALYSIS:")
                print(f"  🌐 Language Score: {analysis['language_score']:.1f}/100 {'✅' if analysis['language_score'] >= 80 else '⚠️' if analysis['language_score'] >= 60 else '❌'}")
                print(f"  🎭 Cultural Score: {analysis['cultural_score']:.1f}/100 {'✅' if analysis['cultural_score'] >= 80 else '⚠️' if analysis['cultural_score'] >= 60 else '❌'}")
                print(f"  🎯 Localization Score: {analysis['localization_score']:.1f}/100 {'✅' if analysis['localization_score'] >= 80 else '⚠️' if analysis['localization_score'] >= 60 else '❌'}")
                print(f"  🏆 Overall Score: {analysis['overall_score']:.1f}/100 {'✅' if analysis['overall_score'] >= 80 else '⚠️' if analysis['overall_score'] >= 60 else '❌'}")
                
                # Show sample content
                if listing.title:
                    print(f"\n📝 TITLE ({market_config['expected_language']}):")
                    print(f"   {listing.title}")
                
                if listing.bullet_points:
                    bullets = listing.bullet_points.split('\n')[:2]
                    print(f"\n🎯 SAMPLE BULLETS:")
                    for i, bullet in enumerate(bullets):
                        if bullet.strip():
                            print(f"   {i+1}. {bullet.strip()}")
                
                if listing.long_description:
                    print(f"\n📄 DESCRIPTION PREVIEW:")
                    preview = listing.long_description[:200] + "..." if len(listing.long_description) > 200 else listing.long_description
                    print(f"   {preview}")
                
                # Language quality check
                all_content = f"{listing.title} {listing.bullet_points} {listing.long_description}".lower()
                
                # Check for expected language elements
                native_found = [word for word in market_config['sample_words'] if word in all_content]
                english_found = [word for word in market_config['avoid_words'] if word in all_content]
                
                print(f"\n🔍 LANGUAGE ANALYSIS:")
                print(f"   {market_config['expected_language']} elements found: {len(native_found)} {native_found[:5]}")
                if english_found:
                    print(f"   ⚠️ English contamination: {len(english_found)} {english_found[:3]}")
                else:
                    print(f"   ✅ No English contamination detected")
                
                # Show issues
                if analysis['issues']:
                    print(f"\n⚠️ ISSUES FOUND:")
                    for issue in analysis['issues'][:5]:
                        print(f"   {issue}")
                
                self.results[market_code] = {
                    'market_name': market_name,
                    'analysis': analysis,
                    'sample_content': {
                        'title': listing.title[:100] + "..." if listing.title and len(listing.title) > 100 else listing.title,
                        'bullet_preview': bullets[0] if bullets else None
                    }
                }
                
                return analysis
                
            else:
                print(f"❌ Listing generation failed: {listing.status if listing else 'Not found'}")
                self.results[market_code] = {
                    'market_name': market_name, 
                    'analysis': {'overall_score': 0, 'issues': ['Generation failed']}
                }
                return None
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            self.results[market_code] = {
                'market_name': market_name,
                'analysis': {'overall_score': 0, 'issues': [f'Error: {e}']}
            }
            return None
    
    def run_all_markets(self):
        """Test all international markets"""
        print("🌍 COMPREHENSIVE INTERNATIONAL MARKETPLACE TESTING")
        print("="*80)
        print("Testing major Amazon markets for language localization quality")
        
        for market_code in self.markets.keys():
            result = self.test_market(market_code)
            time.sleep(5)  # Delay between markets
            
        # Generate comprehensive report
        self.generate_localization_report()
    
    def generate_localization_report(self):
        """Generate detailed international localization report"""
        print(f"\n{'='*80}")
        print("🌍 INTERNATIONAL LOCALIZATION QUALITY REPORT")
        print(f"{'='*80}")
        
        if not self.results:
            print("❌ No results to analyze")
            return
        
        # Overall statistics
        scores = []
        excellent_markets = 0
        good_markets = 0
        poor_markets = 0
        
        print(f"\n🌐 MARKET-BY-MARKET RESULTS:")
        print("-" * 80)
        
        for market_code, result in self.results.items():
            market_name = result['market_name']
            analysis = result['analysis']
            score = analysis.get('overall_score', 0)
            scores.append(score)
            
            if score >= 90:
                grade = "A+"
                status = "✅"
                excellent_markets += 1
            elif score >= 80:
                grade = "A"
                status = "✅"
                good_markets += 1
            elif score >= 70:
                grade = "B" 
                status = "⚠️"
                good_markets += 1
            elif score >= 60:
                grade = "C"
                status = "⚠️"
            else:
                grade = "D"
                status = "❌"
                poor_markets += 1
            
            print(f"{status} {market_name:20} ({market_code}) - {score:5.1f}/100 (Grade: {grade})")
            
            # Show sample if available
            if 'sample_content' in result and result['sample_content']['title']:
                print(f"     Sample: {result['sample_content']['title'][:60]}...")
        
        # Summary statistics  
        avg_score = sum(scores) / len(scores) if scores else 0
        print(f"\n📊 SUMMARY STATISTICS:")
        print(f"  Average Localization Score: {avg_score:.1f}/100")
        print(f"  Excellent Markets (90+): {excellent_markets}")
        print(f"  Good Markets (70-89):    {good_markets}")
        print(f"  Poor Markets (<70):      {poor_markets}")
        
        # Category breakdown
        categories = ['language_score', 'cultural_score', 'localization_score']
        category_names = ['Language Accuracy', 'Cultural Adaptation', 'Localization Quality']
        
        print(f"\n🔍 CATEGORY BREAKDOWN:")
        for i, category in enumerate(categories):
            cat_scores = []
            for result in self.results.values():
                if isinstance(result.get('analysis'), dict):
                    cat_scores.append(result['analysis'].get(category, 0))
            cat_avg = sum(cat_scores) / len(cat_scores) if cat_scores else 0
            print(f"  {category_names[i]:20}: {cat_avg:5.1f}/100")
        
        # Common issues
        all_issues = []
        for result in self.results.values():
            if isinstance(result.get('analysis'), dict) and 'issues' in result['analysis']:
                all_issues.extend(result['analysis']['issues'])
        
        if all_issues:
            from collections import Counter
            issue_counts = Counter(all_issues)
            print(f"\n⚠️ MOST COMMON LOCALIZATION ISSUES:")
            for issue, count in issue_counts.most_common(5):
                print(f"  {count}x - {issue}")
        
        # Recommendations
        print(f"\n🎯 LOCALIZATION OPTIMIZATION RECOMMENDATIONS:")
        if avg_score >= 85:
            print("✅ EXCELLENT: International localization working at professional level")
        elif avg_score >= 75:
            print("⚠️ GOOD: Minor improvements needed for 10/10 international quality")
            print("  - Enhance cultural elements for each market")
            print("  - Improve language-specific terminology")
        elif avg_score >= 60:
            print("⚠️ NEEDS IMPROVEMENT: Several markets require attention")
            print("  - Strengthen language accuracy requirements")
            print("  - Add market-specific cultural adaptations")
            print("  - Improve localization prompt specificity")
        else:
            print("❌ CRITICAL: Major international system overhaul needed")
            print("  - Redesign language-specific prompts")
            print("  - Add comprehensive cultural guidelines")
            print("  - Implement better language validation")
        
        # Market-specific recommendations
        print(f"\n🌍 MARKET-SPECIFIC RECOMMENDATIONS:")
        for market_code, result in self.results.items():
            score = result['analysis'].get('overall_score', 0)
            if score < 70:
                print(f"  {result['market_name']:15}: Needs significant localization improvement")
            elif score < 85:
                print(f"  {result['market_name']:15}: Minor cultural adaptation needed")
        
        # Save report
        report_file = f"international_localization_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, default=str, ensure_ascii=False)
        print(f"\n💾 Detailed report saved: {report_file}")
        
        return avg_score

if __name__ == "__main__":
    print("Starting International Marketplace Testing...")
    tester = InternationalMarketTester()
    
    # Option to test single market or all
    if len(sys.argv) > 1:
        market = sys.argv[1].lower()
        if market in tester.markets:
            tester.test_market(market)
        else:
            print(f"Invalid market. Choose from: {', '.join(tester.markets.keys())}")
    else:
        # Test all markets
        final_score = tester.run_all_markets()
        if final_score and final_score >= 80:
            print(f"\n🎉 SUCCESS: International localization optimized to {final_score:.1f}/100!")
        else:
            print(f"\n⚠️ Additional localization optimization needed.")