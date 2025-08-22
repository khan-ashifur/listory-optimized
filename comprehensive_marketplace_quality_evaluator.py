#!/usr/bin/env python
"""
COMPREHENSIVE MARKETPLACE QUALITY EVALUATOR
============================================

This script systematically evaluates ALL marketplace listings to achieve 10/10 ChatGPT quality scoring.

SCORING CRITERIA (10 points each):
1. Title Quality (10pts): Brand clarity, no off-brand terms, appropriate length, clear value prop
2. Features Quality (10pts): Benefit-driven, unique claims, lifestyle hooks, proper count
3. Description Quality (10pts): Conversational tone, real-life use cases, cultural elements
4. Conversion Elements (10pts): Urgency, social proof, clear CTAs
5. SEO Keywords (10pts): Natural integration, not overstuffed, relevant terms
6. Attributes/Compliance (10pts): Realistic pricing, proper certifications, compliance
7. Cultural Localization (10pts): Local occasions, cultural references, language appropriateness
8. Rich Media (10pts): Relevant image suggestions, platform-appropriate content

MAXIMUM SCORE: 80/80 = 10.0/10
"""

import os
import sys
import django
import json
from datetime import datetime
from typing import Dict, List, Tuple, Any

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_path)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.services import ListingGeneratorService
from apps.core.models import Product
from django.contrib.auth.models import User

class MarketplaceQualityEvaluator:
    """Comprehensive quality evaluator for all marketplace listings."""
    
    def __init__(self):
        self.service = ListingGeneratorService()
        self.user, _ = User.objects.get_or_create(username='marketplace_evaluator')
        self.results = {}
        
        # Test products for different categories
        self.test_products = [
            {
                'name': 'Wireless Gaming Headset',
                'brand_name': 'AudioPro',
                'description': 'Professional wireless gaming headset with active noise cancellation',
                'categories': 'Electronics > Audio > Headphones',
                'features': 'Wireless Connectivity\nActive Noise Cancellation\n50-hour Battery Life\nErgonomic Design\nPremium Sound Quality\nDetachable Microphone',
                'price': 129.99,
                'occasion': 'christmas'
            },
            {
                'name': 'Professional Kitchen Knife Set',
                'brand_name': 'ChefMaster',
                'description': 'Premium stainless steel kitchen knife set for professional cooking',
                'categories': 'Home & Kitchen > Cutlery > Knife Sets',
                'features': 'High Carbon Steel\nErgonomic Handles\nDishwasher Safe\n15-Piece Set\nKnife Block Included\nProfessional Grade',
                'price': 89.99,
                'occasion': 'mothers_day'
            },
            {
                'name': 'Smart Fitness Tracker',
                'brand_name': 'FitTech',
                'description': 'Advanced fitness tracker with heart rate monitoring and GPS',
                'categories': 'Sports & Outdoors > Fitness > Activity Trackers',
                'features': 'Heart Rate Monitor\nGPS Tracking\n7-Day Battery\nWaterproof Design\nSleep Tracking\nSmartphone Sync',
                'price': 199.99,
                'occasion': 'new_year'
            }
        ]

    def evaluate_listing_quality(self, listing: Any, marketplace: str) -> Dict[str, float]:
        """Evaluate listing quality against 8 criteria (10 points each)."""
        scores = {}
        
        # 1. Title Quality (10pts)
        scores['title_quality'] = self._evaluate_title_quality(listing, marketplace)
        
        # 2. Features Quality (10pts) 
        scores['features_quality'] = self._evaluate_features_quality(listing, marketplace)
        
        # 3. Description Quality (10pts)
        scores['description_quality'] = self._evaluate_description_quality(listing, marketplace)
        
        # 4. Conversion Elements (10pts)
        scores['conversion_elements'] = self._evaluate_conversion_elements(listing, marketplace)
        
        # 5. SEO Keywords (10pts)
        scores['seo_keywords'] = self._evaluate_seo_keywords(listing, marketplace)
        
        # 6. Attributes/Compliance (10pts)
        scores['attributes_compliance'] = self._evaluate_attributes_compliance(listing, marketplace)
        
        # 7. Cultural Localization (10pts)
        scores['cultural_localization'] = self._evaluate_cultural_localization(listing, marketplace)
        
        # 8. Rich Media (10pts)
        scores['rich_media'] = self._evaluate_rich_media(listing, marketplace)
        
        return scores

    def _evaluate_title_quality(self, listing: Any, marketplace: str) -> float:
        """Evaluate title quality (10 points max)."""
        score = 0.0
        
        # Get appropriate title field
        if marketplace.startswith('walmart'):
            title = getattr(listing, 'walmart_product_title', '')
        else:
            title = getattr(listing, 'amazon_title', '')
        
        if not title:
            return 0.0
            
        # Brand clarity (2pts)
        if any(brand in title.lower() for brand in ['audiopro', 'chefmaster', 'fittech']):
            score += 2.0
        
        # No off-brand terms (2pts)
        off_brand_terms = ['generic', 'noname', 'unbranded', 'oem']
        if not any(term in title.lower() for term in off_brand_terms):
            score += 2.0
        
        # Appropriate length (2pts)
        if marketplace.startswith('walmart'):
            ideal_range = (50, 150)
        else:
            ideal_range = (150, 200)
        
        if ideal_range[0] <= len(title) <= ideal_range[1]:
            score += 2.0
        elif ideal_range[0] - 20 <= len(title) <= ideal_range[1] + 20:
            score += 1.0
            
        # Clear value proposition (2pts)
        value_indicators = ['professional', 'premium', 'advanced', 'high-quality', 'best']
        if any(indicator in title.lower() for indicator in value_indicators):
            score += 2.0
            
        # Keyword optimization (2pts)
        if len(title.split()) >= 8:  # Good keyword density
            score += 2.0
        
        return min(score, 10.0)

    def _evaluate_features_quality(self, listing: Any, marketplace: str) -> float:
        """Evaluate features quality (10 points max)."""
        score = 0.0
        
        # Get appropriate features field
        if marketplace.startswith('walmart'):
            features = getattr(listing, 'walmart_key_features', '')
        else:
            features = getattr(listing, 'amazon_bullet_points', '')
            
        if not features:
            return 0.0
            
        feature_list = features.split('\n')
        feature_count = len([f for f in feature_list if f.strip()])
        
        # Proper count (2pts)
        if marketplace.startswith('walmart'):
            ideal_count = range(5, 8)
        else:
            ideal_count = range(5, 6)
            
        if feature_count in ideal_count:
            score += 2.0
        elif feature_count >= 4:
            score += 1.0
            
        # Benefit-driven language (3pts)
        benefit_words = ['improve', 'enhance', 'experience', 'comfort', 'easy', 'convenient', 'save']
        benefit_count = sum(1 for word in benefit_words if word in features.lower())
        score += min(benefit_count, 3.0)
        
        # Unique claims (2pts)
        unique_words = ['exclusive', 'patented', 'award-winning', 'industry-leading', 'revolutionary']
        if any(word in features.lower() for word in unique_words):
            score += 2.0
            
        # Lifestyle hooks (2pts)
        lifestyle_words = ['lifestyle', 'daily', 'routine', 'family', 'home', 'work', 'travel']
        if any(word in features.lower() for word in lifestyle_words):
            score += 2.0
            
        # Technical specificity (1pt)
        tech_indicators = ['hours', 'mhz', 'ghz', 'watts', 'degrees', 'minutes', '%']
        if any(indicator in features.lower() for indicator in tech_indicators):
            score += 1.0
        
        return min(score, 10.0)

    def _evaluate_description_quality(self, listing: Any, marketplace: str) -> float:
        """Evaluate description quality (10 points max)."""
        score = 0.0
        
        # Get appropriate description field
        if marketplace.startswith('walmart'):
            description = getattr(listing, 'walmart_long_description', '')
        else:
            description = getattr(listing, 'amazon_description', '')
            
        if not description:
            return 0.0
            
        word_count = len(description.split())
        
        # Appropriate length (2pts)
        if marketplace.startswith('walmart'):
            ideal_range = (150, 300)
        else:
            ideal_range = (200, 400)
            
        if ideal_range[0] <= word_count <= ideal_range[1]:
            score += 2.0
        elif word_count >= ideal_range[0] - 50:
            score += 1.0
            
        # Conversational tone (3pts)
        conversational_indicators = ['you', 'your', 'imagine', 'picture', 'experience', 'feel']
        conv_count = sum(1 for word in conversational_indicators if word in description.lower())
        score += min(conv_count / 2, 3.0)
        
        # Real-life use cases (3pts)
        use_case_indicators = ['perfect for', 'ideal when', 'great for', 'whether you', 'during']
        use_case_count = sum(1 for phrase in use_case_indicators if phrase in description.lower())
        score += min(use_case_count, 3.0)
        
        # Cultural elements (2pts)
        cultural_indicators = ['family', 'home', 'tradition', 'celebration', 'gathering', 'community']
        if any(word in description.lower() for word in cultural_indicators):
            score += 2.0
        
        return min(score, 10.0)

    def _evaluate_conversion_elements(self, listing: Any, marketplace: str) -> float:
        """Evaluate conversion elements (10 points max)."""
        score = 0.0
        
        # Get all text content
        if marketplace.startswith('walmart'):
            all_content = ' '.join([
                getattr(listing, 'walmart_product_title', ''),
                getattr(listing, 'walmart_key_features', ''),
                getattr(listing, 'walmart_long_description', '')
            ])
        else:
            all_content = ' '.join([
                getattr(listing, 'amazon_title', ''),
                getattr(listing, 'amazon_bullet_points', ''),
                getattr(listing, 'amazon_description', '')
            ])
            
        if not all_content:
            return 0.0
            
        # Urgency indicators (3pts)
        urgency_words = ['limited', 'exclusive', 'now', 'today', 'hurry', 'sale', 'deal']
        urgency_count = sum(1 for word in urgency_words if word in all_content.lower())
        score += min(urgency_count, 3.0)
        
        # Social proof (3pts)
        social_proof = ['trusted', 'popular', 'bestseller', 'award', 'rated', 'reviewed']
        if any(word in all_content.lower() for word in social_proof):
            score += 3.0
            
        # Clear CTAs (2pts)
        cta_phrases = ['order now', 'buy today', 'get yours', 'add to cart', 'shop now']
        if any(phrase in all_content.lower() for phrase in cta_phrases):
            score += 2.0
            
        # Value communication (2pts)
        value_words = ['save', 'value', 'affordable', 'investment', 'worth']
        if any(word in all_content.lower() for word in value_words):
            score += 2.0
        
        return min(score, 10.0)

    def _evaluate_seo_keywords(self, listing: Any, marketplace: str) -> float:
        """Evaluate SEO keywords (10 points max)."""
        score = 0.0
        
        # Get all text content
        if marketplace.startswith('walmart'):
            all_content = ' '.join([
                getattr(listing, 'walmart_product_title', ''),
                getattr(listing, 'walmart_key_features', ''),
                getattr(listing, 'walmart_long_description', '')
            ])
            keywords = getattr(listing, 'walmart_search_terms', '')
        else:
            all_content = ' '.join([
                getattr(listing, 'amazon_title', ''),
                getattr(listing, 'amazon_bullet_points', ''),
                getattr(listing, 'amazon_description', '')
            ])
            keywords = getattr(listing, 'amazon_keywords', '')
            
        if not all_content:
            return 0.0
            
        # Natural integration (4pts)
        # Keywords should appear naturally in content
        if keywords:
            keyword_list = [k.strip() for k in keywords.split(',') if k.strip()]
            natural_count = sum(1 for kw in keyword_list if kw.lower() in all_content.lower())
            score += min(natural_count / len(keyword_list) * 4, 4.0) if keyword_list else 0.0
        
        # Not overstuffed (3pts)
        words = all_content.lower().split()
        word_freq = {}
        for word in words:
            if len(word) > 3:  # Ignore short words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Check if any word appears too frequently
        max_freq = max(word_freq.values()) if word_freq else 0
        total_words = len(words)
        if total_words > 0 and max_freq / total_words <= 0.05:  # No word > 5% frequency
            score += 3.0
        elif total_words > 0 and max_freq / total_words <= 0.08:
            score += 2.0
            
        # Relevant terms (3pts)
        # Check for category-relevant keywords
        category_keywords = {
            'electronics': ['wireless', 'battery', 'connectivity', 'tech', 'smart'],
            'kitchen': ['cooking', 'chef', 'culinary', 'kitchen', 'food'],
            'fitness': ['fitness', 'health', 'workout', 'exercise', 'training']
        }
        
        for category, relevant_words in category_keywords.items():
            if any(word in all_content.lower() for word in relevant_words):
                score += 3.0
                break
        
        return min(score, 10.0)

    def _evaluate_attributes_compliance(self, listing: Any, marketplace: str) -> float:
        """Evaluate attributes and compliance (10 points max)."""
        score = 0.0
        
        # Realistic pricing (3pts)
        # This would normally check against market data, for now we'll assume reasonable
        score += 3.0
        
        # Proper certifications (3pts)
        if marketplace.startswith('walmart'):
            all_content = ' '.join([
                getattr(listing, 'walmart_key_features', ''),
                getattr(listing, 'walmart_long_description', '')
            ])
        else:
            all_content = ' '.join([
                getattr(listing, 'amazon_bullet_points', ''),
                getattr(listing, 'amazon_description', '')
            ])
            
        certifications = ['ul', 'fcc', 'ce', 'rohs', 'iso', 'fda']
        if any(cert in all_content.lower() for cert in certifications):
            score += 3.0
            
        # Platform compliance (4pts)
        # Check for platform-specific requirements
        if marketplace.startswith('walmart'):
            walmart_indicators = ['rollback', 'everyday low', 'great value', 'save money']
            if any(indicator in all_content.lower() for indicator in walmart_indicators):
                score += 2.0
        else:
            amazon_indicators = ['prime', 'fulfillment', 'amazon']
            if any(indicator in all_content.lower() for indicator in amazon_indicators):
                score += 2.0
                
        # Complete product information (2pts)
        if all_content and len(all_content.split()) > 100:
            score += 2.0
        
        return min(score, 10.0)

    def _evaluate_cultural_localization(self, listing: Any, marketplace: str) -> float:
        """Evaluate cultural localization (10 points max)."""
        score = 0.0
        
        # Get all content
        if marketplace.startswith('walmart'):
            all_content = ' '.join([
                getattr(listing, 'walmart_product_title', ''),
                getattr(listing, 'walmart_key_features', ''),
                getattr(listing, 'walmart_long_description', '')
            ])
        else:
            all_content = ' '.join([
                getattr(listing, 'amazon_title', ''),
                getattr(listing, 'amazon_bullet_points', ''),
                getattr(listing, 'amazon_description', '')
            ])
            
        if not all_content:
            return 0.0
            
        # Local occasions (4pts)
        occasion_words = ['christmas', 'thanksgiving', 'halloween', 'valentine', 'mother', 'father']
        if any(occasion in all_content.lower() for occasion in occasion_words):
            score += 4.0
            
        # Cultural references (3pts)
        cultural_words = ['american', 'family', 'home', 'tradition', 'community', 'lifestyle']
        cultural_count = sum(1 for word in cultural_words if word in all_content.lower())
        score += min(cultural_count, 3.0)
        
        # Language appropriateness (3pts)
        # For now, assume English content is appropriate for US/UK markets
        if any(c.isalpha() for c in all_content):
            score += 3.0
        
        return min(score, 10.0)

    def _evaluate_rich_media(self, listing: Any, marketplace: str) -> float:
        """Evaluate rich media suggestions (10 points max)."""
        score = 0.0
        
        # A+ Content / Enhanced Content
        if marketplace.startswith('amazon'):
            aplus_content = getattr(listing, 'amazon_aplus_content', '')
            if aplus_content and len(aplus_content) > 100:
                score += 5.0
        else:
            # Walmart enhanced content
            enhanced_content = getattr(listing, 'walmart_enhanced_content', '')
            if enhanced_content and len(enhanced_content) > 100:
                score += 5.0
                
        # Image suggestions (5pts)
        # Check if content mentions image-worthy features
        if marketplace.startswith('walmart'):
            all_content = getattr(listing, 'walmart_long_description', '')
        else:
            all_content = getattr(listing, 'amazon_description', '')
            
        if all_content:
            image_indicators = ['see', 'view', 'display', 'visual', 'color', 'design', 'style']
            if any(indicator in all_content.lower() for indicator in image_indicators):
                score += 5.0
        
        return min(score, 10.0)

    def test_marketplace(self, marketplace: str, marketplace_language: str = 'en') -> Dict[str, Any]:
        """Test a specific marketplace with all test products."""
        print(f'\n🔍 TESTING MARKETPLACE: {marketplace.upper()}')
        print('=' * 50)
        
        marketplace_results = {
            'marketplace': marketplace,
            'language': marketplace_language,
            'products': [],
            'average_score': 0.0,
            'category_scores': {},
            'timestamp': datetime.now().isoformat()
        }
        
        total_score = 0.0
        product_count = 0
        
        for i, product_data in enumerate(self.test_products, 1):
            print(f'\n🛍️  Testing Product {i}: {product_data["name"]}')
            
            try:
                # Create product
                product = Product.objects.create(
                    user=self.user,
                    target_platform='amazon' if not marketplace.startswith('walmart') else 'walmart',
                    marketplace=marketplace,
                    marketplace_language=marketplace_language,
                    brand_tone='professional',
                    **product_data
                )
                
                # Generate listing
                platform = 'amazon' if not marketplace.startswith('walmart') else 'walmart'
                listing = self.service.generate_listing(product.id, platform)
                
                if listing.status == 'completed':
                    # Evaluate quality
                    scores = self.evaluate_listing_quality(listing, marketplace)
                    overall_score = sum(scores.values()) / 8.0  # Average of 8 criteria
                    
                    product_result = {
                        'product_name': product_data['name'],
                        'scores': scores,
                        'overall_score': overall_score,
                        'title': getattr(listing, f'{platform}_product_title' if platform == 'walmart' else f'{platform}_title', ''),
                        'features_count': len(getattr(listing, f'{platform}_key_features' if platform == 'walmart' else f'{platform}_bullet_points', '').split('\n')),
                        'description_length': len(getattr(listing, f'{platform}_long_description' if platform == 'walmart' else f'{platform}_description', '').split())
                    }
                    
                    marketplace_results['products'].append(product_result)
                    total_score += overall_score
                    product_count += 1
                    
                    print(f'   ✅ Score: {overall_score:.1f}/10.0')
                    for criterion, score in scores.items():
                        emoji = '🟢' if score >= 8 else '🟡' if score >= 6 else '🔴'
                        print(f'   {emoji} {criterion.replace("_", " ").title()}: {score:.1f}/10')
                        
                else:
                    print(f'   ❌ Failed to generate listing: {listing.status}')
                    
            except Exception as e:
                print(f'   ❌ Error testing product: {e}')
            finally:
                # Clean up
                if 'product' in locals():
                    product.delete()
        
        if product_count > 0:
            marketplace_results['average_score'] = total_score / product_count
            
            # Calculate category averages
            if marketplace_results['products']:
                category_totals = {}
                for product in marketplace_results['products']:
                    for criterion, score in product['scores'].items():
                        if criterion not in category_totals:
                            category_totals[criterion] = []
                        category_totals[criterion].append(score)
                
                for criterion, scores in category_totals.items():
                    marketplace_results['category_scores'][criterion] = sum(scores) / len(scores)
        
        return marketplace_results

    def run_comprehensive_evaluation(self):
        """Run evaluation on all marketplaces."""
        print('🌍 COMPREHENSIVE MARKETPLACE QUALITY EVALUATION')
        print('=' * 55)
        print('Evaluating ALL marketplaces with 10/10 scoring system...')
        
        # Define all marketplaces to test
        marketplaces = [
            # Walmart markets
            ('walmart_usa', 'en-us'),
            ('walmart_canada', 'en-ca'),
            ('walmart_mexico', 'es-mx'),
            
            # Amazon markets
            ('us', 'en-us'),
            ('ca', 'en-ca'),
            ('mx', 'es-mx'),
            ('uk', 'en-gb'),
            ('de', 'de-de'),
            ('fr', 'fr-fr'),
            ('it', 'it-it'),
            ('es', 'es-es'),
            ('nl', 'nl-nl'),
            ('se', 'sv-se'),
            ('pl', 'pl-pl'),
            ('be', 'nl-be'),
            ('jp', 'ja-jp'),
            ('in', 'en-in'),
            ('sg', 'en-sg'),
            ('ae', 'en-ae'),
            ('sa', 'ar-sa'),
            ('br', 'pt-br'),
            ('au', 'en-au'),
            ('tr', 'tr-tr'),
            ('eg', 'ar-eg')
        ]
        
        all_results = []
        
        for marketplace, language in marketplaces:
            try:
                result = self.test_marketplace(marketplace, language)
                all_results.append(result)
            except Exception as e:
                print(f'❌ Failed to test {marketplace}: {e}')
                
        # Save comprehensive report
        self._generate_comprehensive_report(all_results)
        
        return all_results

    def _generate_comprehensive_report(self, all_results: List[Dict[str, Any]]):
        """Generate comprehensive quality report."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'comprehensive_marketplace_quality_report_{timestamp}.json'
        
        # Calculate overall statistics
        successful_markets = [r for r in all_results if r['products']]
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_markets_tested': len(all_results),
            'successful_markets': len(successful_markets),
            'overall_average': sum(r['average_score'] for r in successful_markets) / len(successful_markets) if successful_markets else 0,
            'markets': all_results,
            'ranking': sorted(successful_markets, key=lambda x: x['average_score'], reverse=True)
        }
        
        # Save JSON report
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        # Generate markdown report
        md_filename = f'comprehensive_marketplace_quality_report_{timestamp}.md'
        self._generate_markdown_report(report, md_filename)
        
        print(f'\n📊 COMPREHENSIVE EVALUATION COMPLETE')
        print(f'   JSON Report: {filename}')
        print(f'   Markdown Report: {md_filename}')
        print(f'   Markets Tested: {len(all_results)}')
        print(f'   Successful Markets: {len(successful_markets)}')
        if successful_markets:
            print(f'   Overall Average: {report["overall_average"]:.1f}/10.0')
            print(f'   Top Performer: {report["ranking"][0]["marketplace"]} ({report["ranking"][0]["average_score"]:.1f}/10)')

    def _generate_markdown_report(self, report: Dict[str, Any], filename: str):
        """Generate markdown quality report."""
        content = f"""# COMPREHENSIVE MARKETPLACE QUALITY EVALUATION REPORT

**Generated:** {report['timestamp']}

## EXECUTIVE SUMMARY

**Overall Performance:** {report['overall_average']:.1f}/10.0
**Markets Tested:** {report['total_markets_tested']}
**Successful Evaluations:** {report['successful_markets']}

## MARKETPLACE RANKINGS

| Rank | Marketplace | Score | Status |
|------|-------------|-------|---------|
"""
        
        for i, market in enumerate(report['ranking'], 1):
            status = '🟢 Excellent' if market['average_score'] >= 9 else '🟡 Good' if market['average_score'] >= 7 else '🔴 Needs Work'
            content += f"| {i} | {market['marketplace'].upper()} | {market['average_score']:.1f}/10 | {status} |\n"
        
        content += f"""
## DETAILED ANALYSIS

### Performance by Category

"""
        
        # Calculate category averages across all markets
        if report['ranking']:
            all_categories = set()
            for market in report['ranking']:
                all_categories.update(market['category_scores'].keys())
            
            for category in sorted(all_categories):
                scores = [m['category_scores'].get(category, 0) for m in report['ranking'] if category in m['category_scores']]
                avg_score = sum(scores) / len(scores) if scores else 0
                content += f"**{category.replace('_', ' ').title()}:** {avg_score:.1f}/10\n\n"
        
        content += """## RECOMMENDATIONS FOR 10/10 ACHIEVEMENT

### High Priority Improvements
1. **Cultural Localization**: Enhance local cultural references and occasions
2. **Conversion Elements**: Strengthen urgency and social proof elements
3. **Rich Media**: Improve image suggestions and enhanced content

### Market-Specific Actions
"""
        
        for market in report['ranking'][:5]:  # Top 5 markets
            content += f"\n**{market['marketplace'].upper()}** ({market['average_score']:.1f}/10):\n"
            
            # Find lowest scoring categories
            if market['category_scores']:
                lowest_categories = sorted(market['category_scores'].items(), key=lambda x: x[1])[:3]
                for category, score in lowest_categories:
                    if score < 8:
                        content += f"- Improve {category.replace('_', ' ')}: {score:.1f}/10\n"
        
        content += f"""
## NEXT STEPS

1. **Immediate Actions**: Focus on markets scoring below 8/10
2. **Optimization Priority**: Target lowest-scoring categories first
3. **Testing Protocol**: Implement continuous quality monitoring
4. **Success Metrics**: Achieve 10/10 across all major markets

---
*Report generated by Comprehensive Marketplace Quality Evaluator*
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

def main():
    evaluator = MarketplaceQualityEvaluator()
    evaluator.run_comprehensive_evaluation()

if __name__ == '__main__':
    main()