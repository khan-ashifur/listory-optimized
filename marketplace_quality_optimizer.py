#!/usr/bin/env python
"""
MARKETPLACE QUALITY OPTIMIZER
=============================

Correctly evaluates marketplace listings and identifies specific optimization opportunities
to achieve 10/10 quality scoring across all marketplaces.
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

class MarketplaceQualityOptimizer:
    """Optimizes marketplace listings for 10/10 quality."""
    
    def __init__(self):
        self.service = ListingGeneratorService()
        self.user, _ = User.objects.get_or_create(username='quality_optimizer')
        
        # Test products across different categories for comprehensive evaluation
        self.test_products = [
            {
                'name': 'Professional Gaming Headset',
                'brand_name': 'AudioPro',
                'description': 'Professional wireless gaming headset with active noise cancellation for immersive gaming experience',
                'categories': 'Electronics > Audio > Gaming Headphones',
                'features': 'Wireless 2.4GHz Connection\nActive Noise Cancellation\n50-Hour Battery Life\nErgonomic Over-Ear Design\nHigh-Fidelity Audio Drivers\nDetachable Boom Microphone',
                'price': 129.99,
                'occasion': 'christmas',
                'brand_tone': 'professional'
            },
            {
                'name': 'Premium Kitchen Knife Set',
                'brand_name': 'ChefMaster',
                'description': 'Professional-grade stainless steel kitchen knife set with ergonomic handles for culinary excellence',
                'categories': 'Home & Kitchen > Cutlery > Knife Sets',
                'features': 'High-Carbon Stainless Steel\nErgonomic Anti-Slip Handles\nDishwasher Safe Construction\n15-Piece Complete Set\nHardwood Storage Block\nProfessional Chef Quality',
                'price': 89.99,
                'occasion': 'mothers_day',
                'brand_tone': 'luxury'
            }
        ]

    def evaluate_listing_quality(self, listing: Any, marketplace: str) -> Dict[str, Any]:
        """Comprehensive quality evaluation using correct field mapping."""
        
        # Get content based on platform type
        if marketplace.startswith('walmart'):
            title = getattr(listing, 'walmart_product_title', '')
            features = getattr(listing, 'walmart_key_features', '')
            description = getattr(listing, 'walmart_description', '')
            search_terms = getattr(listing, 'walmart_search_terms', '')
            
            # Fallback to general fields if walmart-specific are empty
            if not description:
                description = getattr(listing, 'long_description', '')
            if not search_terms:
                search_terms = getattr(listing, 'keywords', '')
        else:
            # Amazon uses general fields
            title = getattr(listing, 'title', '')
            features = getattr(listing, 'bullet_points', '')
            description = getattr(listing, 'long_description', '')
            search_terms = getattr(listing, 'amazon_keywords', '') or getattr(listing, 'keywords', '')
        
        # Content analysis
        content_analysis = {
            'title_length': len(title) if title else 0,
            'features_count': len([f for f in features.split('\n') if f.strip()]) if features else 0,
            'description_word_count': len(description.split()) if description else 0,
            'keywords_count': len([k for k in search_terms.split(',') if k.strip()]) if search_terms else 0,
            'has_title': bool(title and len(title.strip()) > 0),
            'has_features': bool(features and len(features.strip()) > 0),
            'has_description': bool(description and len(description.strip()) > 0),
            'has_keywords': bool(search_terms and len(search_terms.strip()) > 0)
        }
        
        # Quality scoring (8 categories × 10 points each = 80 total)
        scores = {}
        issues = []
        recommendations = []
        
        # 1. Title Quality (0-10 points)
        title_score = 0.0
        if content_analysis['has_title']:
            # Brand presence (2pts)
            if any(brand in title.lower() for brand in ['audiopro', 'chefmaster']):
                title_score += 2.0
            else:
                issues.append("Title missing brand name")
                
            # Length appropriateness (2pts)
            ideal_range = (60, 100) if marketplace.startswith('walmart') else (150, 200)
            if ideal_range[0] <= content_analysis['title_length'] <= ideal_range[1]:
                title_score += 2.0
            elif content_analysis['title_length'] > 0:
                title_score += 1.0
                issues.append(f"Title length ({content_analysis['title_length']}) not optimal for {marketplace}")
                
            # Value proposition (2pts)
            value_words = ['professional', 'premium', 'advanced', 'high-quality', 'superior']
            if any(word in title.lower() for word in value_words):
                title_score += 2.0
            else:
                recommendations.append("Add value proposition words to title")
                
            # Keyword optimization (2pts)
            if len(title.split()) >= 8:
                title_score += 2.0
            else:
                recommendations.append("Optimize title keyword density")
                
            # Marketplace fit (2pts)
            if marketplace.startswith('walmart'):
                walmart_terms = ['value', 'rollback', 'great deal', 'save', 'everyday low']
                if any(term in title.lower() for term in walmart_terms):
                    title_score += 2.0
            else:
                amazon_terms = ['prime eligible', 'fast shipping', 'bestseller']
                if any(term in title.lower() for term in amazon_terms):
                    title_score += 2.0
        else:
            issues.append("Missing title - critical issue")
        
        scores['title_quality'] = title_score
        
        # 2. Features Quality (0-10 points)
        features_score = 0.0
        if content_analysis['has_features']:
            # Proper count (2pts)
            ideal_count = range(5, 8) if marketplace.startswith('walmart') else range(5, 6)
            if content_analysis['features_count'] in ideal_count:
                features_score += 2.0
            elif content_analysis['features_count'] >= 4:
                features_score += 1.0
            else:
                issues.append(f"Insufficient features count: {content_analysis['features_count']}")
                
            # Benefit-driven language (3pts)
            benefit_words = ['enhance', 'improve', 'deliver', 'provide', 'ensure', 'guarantee']
            benefit_count = sum(1 for word in benefit_words if word in features.lower())
            features_score += min(benefit_count * 0.5, 3.0)
            
            # Unique selling points (2pts)
            unique_words = ['exclusive', 'patented', 'award-winning', 'professional-grade', 'industry-leading']
            if any(word in features.lower() for word in unique_words):
                features_score += 2.0
            else:
                recommendations.append("Add unique selling points to features")
                
            # Technical specificity (2pts)
            tech_indicators = ['hour', 'year', 'grade', 'rated', 'certified', 'tested']
            if any(indicator in features.lower() for indicator in tech_indicators):
                features_score += 2.0
            else:
                recommendations.append("Add technical specifications to features")
                
            # Lifestyle appeal (1pt)
            lifestyle_words = ['comfort', 'convenience', 'easy', 'effortless', 'perfect', 'ideal']
            if any(word in features.lower() for word in lifestyle_words):
                features_score += 1.0
        else:
            issues.append("Missing features - critical issue")
        
        scores['features_quality'] = features_score
        
        # 3. Description Quality (0-10 points)
        description_score = 0.0
        if content_analysis['has_description']:
            # Appropriate length (3pts)
            ideal_range = (150, 300) if marketplace.startswith('walmart') else (200, 400)
            if ideal_range[0] <= content_analysis['description_word_count'] <= ideal_range[1]:
                description_score += 3.0
            elif content_analysis['description_word_count'] >= 100:
                description_score += 2.0
            elif content_analysis['description_word_count'] >= 50:
                description_score += 1.0
            else:
                issues.append(f"Description too short: {content_analysis['description_word_count']} words")
                
            # Conversational tone (3pts)
            conv_indicators = ['you', 'your', 'imagine', 'experience', 'discover', 'enjoy']
            conv_count = sum(1 for word in conv_indicators if word in description.lower())
            description_score += min(conv_count * 0.5, 3.0)
            
            # Real-life use cases (2pts)
            use_case_phrases = ['perfect for', 'ideal when', 'great for', 'whether you', 'from']
            if any(phrase in description.lower() for phrase in use_case_phrases):
                description_score += 2.0
            else:
                recommendations.append("Add real-life use cases to description")
                
            # Emotional engagement (2pts)
            emotion_words = ['love', 'amazing', 'incredible', 'transform', 'elevate', 'outstanding']
            if any(word in description.lower() for word in emotion_words):
                description_score += 2.0
            else:
                recommendations.append("Add emotional engagement to description")
        else:
            issues.append("Missing description - critical issue")
        
        scores['description_quality'] = description_score
        
        # 4. Conversion Elements (0-10 points)
        conversion_score = 0.0
        all_content = f"{title} {features} {description}".lower()
        if all_content.strip():
            # Urgency (3pts)
            urgency_words = ['limited', 'exclusive', 'now', 'today', 'hurry', 'sale', 'deal']
            urgency_count = sum(1 for word in urgency_words if word in all_content)
            conversion_score += min(urgency_count, 3.0)
            
            # Social proof (3pts)
            social_words = ['trusted', 'popular', 'bestseller', 'award', 'rated', 'reviewed', 'professional']
            if any(word in all_content for word in social_words):
                conversion_score += 3.0
            else:
                recommendations.append("Add social proof elements")
                
            # Value communication (2pts)
            value_words = ['save', 'value', 'investment', 'worth', 'premium', 'quality']
            if any(word in all_content for word in value_words):
                conversion_score += 2.0
                
            # Trust signals (2pts)
            trust_words = ['guarantee', 'warranty', 'certified', 'tested', 'approved', 'satisfaction']
            if any(word in all_content for word in trust_words):
                conversion_score += 2.0
            else:
                recommendations.append("Add trust signals")
        
        scores['conversion_elements'] = conversion_score
        
        # 5. SEO Keywords (0-10 points)
        seo_score = 0.0
        if content_analysis['has_keywords']:
            # Keyword count (3pts)
            if content_analysis['keywords_count'] >= 10:
                seo_score += 3.0
            elif content_analysis['keywords_count'] >= 5:
                seo_score += 2.0
            elif content_analysis['keywords_count'] >= 3:
                seo_score += 1.0
            else:
                issues.append(f"Insufficient keywords: {content_analysis['keywords_count']}")
                
            # Natural integration (4pts)
            keyword_terms = [k.strip().lower() for k in search_terms.split(',') if k.strip()]
            natural_count = sum(1 for term in keyword_terms if term in all_content)
            integration_rate = natural_count / len(keyword_terms) if keyword_terms else 0
            seo_score += integration_rate * 4.0
            
            # Relevance (3pts) - simplified check for category relevance
            category_words = ['gaming', 'headset', 'kitchen', 'knife', 'professional', 'wireless']
            relevant_keywords = sum(1 for term in keyword_terms for word in category_words if word in term)
            if relevant_keywords >= 3:
                seo_score += 3.0
            elif relevant_keywords >= 1:
                seo_score += 2.0
        else:
            issues.append("Missing keywords - critical SEO issue")
        
        scores['seo_keywords'] = seo_score
        
        # 6. Attributes/Compliance (0-10 points)
        compliance_score = 5.0  # Base score for basic compliance
        
        # Platform-specific compliance (3pts)
        if marketplace.startswith('walmart'):
            walmart_terms = ['rollback', 'great value', 'everyday low', 'save money']
            if any(term in all_content for term in walmart_terms):
                compliance_score += 2.0
        else:
            amazon_terms = ['prime', 'fulfillment', 'fast shipping']
            if any(term in all_content for term in amazon_terms):
                compliance_score += 2.0
                
        # Certifications mentioned (2pts)
        cert_terms = ['ul', 'fcc', 'ce', 'certified', 'approved', 'tested']
        if any(term in all_content for term in cert_terms):
            compliance_score += 2.0
            
        scores['attributes_compliance'] = min(compliance_score, 10.0)
        
        # 7. Cultural Localization (0-10 points)
        cultural_score = 0.0
        
        # Occasion integration (4pts)
        occasion_terms = ['christmas', 'holiday', 'gift', 'mothers day', 'celebration', 'special']
        if any(term in all_content for term in occasion_terms):
            cultural_score += 4.0
        else:
            recommendations.append("Add occasion-specific messaging")
            
        # Cultural values (3pts)
        cultural_terms = ['family', 'home', 'tradition', 'community', 'american', 'quality']
        cultural_count = sum(1 for term in cultural_terms if term in all_content)
        cultural_score += min(cultural_count * 0.5, 3.0)
        
        # Language appropriateness (3pts)
        if marketplace == 'de':
            if 'ü' in all_content or 'ö' in all_content or 'ä' in all_content:
                cultural_score += 3.0
            else:
                issues.append("Missing German language elements")
        elif marketplace == 'fr':
            french_terms = ['qualité', 'professionnel', 'premium']
            if any(term in all_content for term in french_terms):
                cultural_score += 3.0
        else:
            # For English markets, good if content is in English
            cultural_score += 3.0
            
        scores['cultural_localization'] = cultural_score
        
        # 8. Rich Media (0-10 points)
        rich_media_score = 0.0
        
        # A+ Content/Enhanced Content (5pts)
        aplus_content = getattr(listing, 'amazon_aplus_content', '') or getattr(listing, 'hero_content', '')
        if aplus_content and len(aplus_content) > 100:
            rich_media_score += 5.0
        else:
            recommendations.append("Enhance A+ content")
            
        # Image-worthy descriptions (3pts)
        image_terms = ['see', 'view', 'display', 'color', 'design', 'style', 'look']
        if any(term in all_content for term in image_terms):
            rich_media_score += 3.0
            
        # Video potential (2pts)
        video_terms = ['demonstration', 'action', 'performance', 'in use', 'working']
        if any(term in all_content for term in video_terms):
            rich_media_score += 2.0
            
        scores['rich_media'] = rich_media_score
        
        # Calculate overall score
        total_score = sum(scores.values())
        overall_score = (total_score / 80.0) * 10.0  # Convert to 0-10 scale
        
        return {
            'marketplace': marketplace,
            'overall_score': overall_score,
            'category_scores': scores,
            'content_analysis': content_analysis,
            'issues': issues,
            'recommendations': recommendations,
            'status': 'excellent' if overall_score >= 9 else 'good' if overall_score >= 7 else 'needs_improvement'
        }

    def test_marketplace_comprehensive(self, marketplace: str, language: str, platform: str) -> Dict[str, Any]:
        """Test marketplace with multiple products."""
        print(f'\n🔍 TESTING {marketplace.upper()} ({language})')
        print('=' * 50)
        
        results = {
            'marketplace': marketplace,
            'language': language,
            'platform': platform,
            'products': [],
            'average_score': 0.0,
            'summary': {}
        }
        
        for i, product_data in enumerate(self.test_products, 1):
            print(f'\n🛍️  Product {i}: {product_data["name"]}')
            
            try:
                # Create product
                product = Product.objects.create(
                    user=self.user,
                    target_platform=platform,
                    marketplace=marketplace,
                    marketplace_language=language,
                    **product_data
                )
                
                # Generate listing
                listing = self.service.generate_listing(product.id, platform)
                
                if listing.status == 'completed':
                    # Evaluate quality
                    evaluation = self.evaluate_listing_quality(listing, marketplace)
                    results['products'].append(evaluation)
                    
                    # Display results
                    score = evaluation['overall_score']
                    status_emoji = '🟢' if score >= 9 else '🟡' if score >= 7 else '🔴'
                    print(f'   {status_emoji} Overall Score: {score:.1f}/10.0 ({evaluation["status"]})')
                    
                    # Show category breakdown
                    for category, score in evaluation['category_scores'].items():
                        emoji = '🟢' if score >= 8 else '🟡' if score >= 6 else '🔴'
                        print(f'   {emoji} {category.replace("_", " ").title()}: {score:.1f}/10')
                    
                    # Show content stats
                    ca = evaluation['content_analysis']
                    print(f'   📊 Content: T({ca["title_length"]}c) F({ca["features_count"]}) D({ca["description_word_count"]}w) K({ca["keywords_count"]})')
                    
                    # Show top issues
                    if evaluation['issues']:
                        print(f'   ⚠️  Issues: {"; ".join(evaluation["issues"][:3])}')
                        
                else:
                    print(f'   ❌ Generation failed: {listing.status}')
                    
            except Exception as e:
                print(f'   ❌ Error: {str(e)[:100]}')
            finally:
                if 'product' in locals():
                    try:
                        product.delete()
                    except:
                        pass
        
        # Calculate averages
        if results['products']:
            results['average_score'] = sum(p['overall_score'] for p in results['products']) / len(results['products'])
            
            # Category averages
            category_totals = {}
            for product in results['products']:
                for category, score in product['category_scores'].items():
                    if category not in category_totals:
                        category_totals[category] = []
                    category_totals[category].append(score)
            
            results['summary'] = {
                category: sum(scores) / len(scores)
                for category, scores in category_totals.items()
            }
            
            print(f'\n📊 MARKETPLACE SUMMARY:')
            print(f'   Average Score: {results["average_score"]:.1f}/10.0')
            
            # Show weakest categories
            weak_categories = sorted(results['summary'].items(), key=lambda x: x[1])[:3]
            print(f'   Weakest Areas:')
            for category, score in weak_categories:
                print(f'     - {category.replace("_", " ").title()}: {score:.1f}/10')
        
        return results

    def run_marketplace_optimization(self):
        """Run comprehensive marketplace optimization analysis."""
        print('🎯 MARKETPLACE QUALITY OPTIMIZATION ANALYSIS')
        print('=' * 55)
        
        # Priority marketplaces to test
        priority_markets = [
            ('walmart_usa', 'en-us', 'walmart'),
            ('walmart_canada', 'en-ca', 'walmart'), 
            ('walmart_mexico', 'es-mx', 'walmart'),
            ('us', 'en-us', 'amazon'),
            ('uk', 'en-gb', 'amazon'),
            ('ca', 'en-ca', 'amazon'),
            ('de', 'de-de', 'amazon'),
            ('fr', 'fr-fr', 'amazon')
        ]
        
        all_results = []
        
        for marketplace, language, platform in priority_markets:
            try:
                result = self.test_marketplace_comprehensive(marketplace, language, platform)
                all_results.append(result)
            except Exception as e:
                print(f'❌ Failed to test {marketplace}: {e}')
        
        # Generate optimization report
        self._generate_optimization_report(all_results)
        
        return all_results
    
    def _generate_optimization_report(self, results: List[Dict[str, Any]]):
        """Generate comprehensive optimization report."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'marketplace_optimization_report_{timestamp}.md'
        
        # Calculate overall statistics
        successful_results = [r for r in results if r['products']]
        
        content = f"""# MARKETPLACE QUALITY OPTIMIZATION REPORT

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## EXECUTIVE SUMMARY

**Markets Tested:** {len(results)}
**Successful Tests:** {len(successful_results)}
"""
        
        if successful_results:
            overall_avg = sum(r['average_score'] for r in successful_results) / len(successful_results)
            content += f"**Overall Average:** {overall_avg:.1f}/10.0\n\n"
            
            # Ranking
            ranked_markets = sorted(successful_results, key=lambda x: x['average_score'], reverse=True)
            
            content += "## MARKETPLACE RANKINGS\n\n"
            content += "| Rank | Marketplace | Score | Status | Weakest Category |\n"
            content += "|------|-------------|-------|--------|-----------------|\n"
            
            for i, market in enumerate(ranked_markets, 1):
                status = '🟢 Excellent' if market['average_score'] >= 9 else '🟡 Good' if market['average_score'] >= 7 else '🔴 Needs Work'
                
                weakest_category = "N/A"
                if market['summary']:
                    weakest = min(market['summary'].items(), key=lambda x: x[1])
                    weakest_category = f"{weakest[0].replace('_', ' ').title()} ({weakest[1]:.1f})"
                
                content += f"| {i} | {market['marketplace'].upper()} | {market['average_score']:.1f}/10 | {status} | {weakest_category} |\n"
            
            content += f"""
## CRITICAL OPTIMIZATION OPPORTUNITIES

### Markets Needing Immediate Attention (Score < 7.0)
"""
            
            needs_work = [m for m in ranked_markets if m['average_score'] < 7.0]
            for market in needs_work:
                content += f"\n**{market['marketplace'].upper()}** ({market['average_score']:.1f}/10):\n"
                
                if market['summary']:
                    weak_categories = sorted(market['summary'].items(), key=lambda x: x[1])[:3]
                    for category, score in weak_categories:
                        if score < 6:
                            content += f"- 🔴 {category.replace('_', ' ').title()}: {score:.1f}/10\n"
            
            content += f"""
### Top Performing Markets (Score ≥ 8.0)
"""
            
            top_markets = [m for m in ranked_markets if m['average_score'] >= 8.0]
            if not top_markets:
                content += "**⚠️  NO MARKETS CURRENTLY ACHIEVING 8.0+ SCORES**\n\n"
            else:
                for market in top_markets:
                    content += f"- **{market['marketplace'].upper()}**: {market['average_score']:.1f}/10\n"
            
            content += f"""
## CATEGORY ANALYSIS

### Overall Category Performance
"""
            
            # Calculate category averages across all markets
            all_categories = set()
            for market in successful_results:
                if market['summary']:
                    all_categories.update(market['summary'].keys())
            
            category_averages = {}
            for category in all_categories:
                scores = []
                for market in successful_results:
                    if market['summary'] and category in market['summary']:
                        scores.append(market['summary'][category])
                if scores:
                    category_averages[category] = sum(scores) / len(scores)
            
            sorted_categories = sorted(category_averages.items(), key=lambda x: x[1], reverse=True)
            
            for category, avg_score in sorted_categories:
                status = '🟢' if avg_score >= 8 else '🟡' if avg_score >= 6 else '🔴'
                content += f"{status} **{category.replace('_', ' ').title()}**: {avg_score:.1f}/10\n\n"
            
            content += f"""
## IMPLEMENTATION ROADMAP

### Phase 1: Critical Fixes (Week 1)
1. **Content Generation Issues**: Fix missing description and keyword fields
2. **Walmart Optimization**: Implement Walmart-specific terminology and value messaging
3. **Feature Enhancement**: Improve benefit-driven language in bullet points

### Phase 2: Quality Improvements (Week 2-3)  
1. **SEO Optimization**: Enhance keyword integration and density
2. **Cultural Localization**: Add region-specific occasions and cultural references
3. **Conversion Elements**: Strengthen urgency, social proof, and trust signals

### Phase 3: Excellence Achievement (Week 4)
1. **Rich Media**: Enhance A+ content and image optimization
2. **Final Testing**: Verify 10/10 scores across all markets
3. **Performance Monitoring**: Implement continuous quality tracking

### Success Metrics
- **Target**: All major markets achieving 9.0+/10 scores
- **Priority Markets**: Walmart USA, Amazon US, Amazon UK, Amazon DE
- **Timeline**: 4 weeks to full optimization

---
*Generated by Marketplace Quality Optimizer*
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f'\n📋 OPTIMIZATION REPORT GENERATED: {filename}')
        if successful_results:
            print(f'   Overall Average: {overall_avg:.1f}/10.0')
            print(f'   Best Market: {ranked_markets[0]["marketplace"]} ({ranked_markets[0]["average_score"]:.1f}/10)')
            print(f'   Markets Needing Work: {len(needs_work)}/{len(successful_results)}')

def main():
    optimizer = MarketplaceQualityOptimizer()
    optimizer.run_marketplace_optimization()

if __name__ == '__main__':
    main()