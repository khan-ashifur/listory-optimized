#!/usr/bin/env python3
"""
Comprehensive All Markets Listing Generator Test
Tests all marketplace systems against 10/10 quality standards
"""

import os
import sys
import django
from datetime import datetime

# Add the backend directory to Python path
backend_path = os.path.join(os.getcwd(), 'backend')
sys.path.insert(0, backend_path)

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.services import ListingGeneratorService
from apps.core.models import Product
from django.contrib.auth.models import User

def analyze_listing_quality(listing, product_data, marketplace):
    """Comprehensive quality analysis for any marketplace"""
    
    scores = {
        'title_quality': 0,
        'features_quality': 0,
        'description_quality': 0,
        'keywords_quality': 0,
        'marketplace_optimization': 0,
        'occasion_integration': 0,
        'brand_tone_alignment': 0,
        'cultural_localization': 0
    }
    
    # Get the correct title field based on marketplace
    if marketplace.startswith('walmart'):
        title = listing.walmart_product_title
        features = listing.walmart_key_features
        description = listing.walmart_description
        keywords = listing.keywords
    else:  # Amazon markets
        title = listing.amazon_title
        features = listing.amazon_bullet_points
        description = listing.amazon_description
        keywords = listing.amazon_keywords
    
    # 1. Title Quality Analysis (Max 10 points)
    if title:
        title_score = 0
        if len(title) >= 50 and len(title) <= 150:  # Optimal length range
            title_score += 3
        if product_data['brand_name'] in title:  # Brand included
            title_score += 2
        if any(word in title.lower() for word in ['premium', 'professional', 'advanced', 'best']):  # Power words
            title_score += 2
        if product_data['occasion'] in title.lower():  # Occasion integration
            title_score += 2
        if any(word in title.lower() for word in ['deal', 'special', 'exclusive']):  # Value terms
            title_score += 1
        scores['title_quality'] = min(title_score, 10)
    
    # 2. Features Quality Analysis (Max 10 points)
    if features:
        features_list = features.split('\n') if isinstance(features, str) else features
        feature_score = 0
        if len(features_list) >= 5:  # Good count
            feature_score += 3
        if all(len(f.strip()) >= 30 for f in features_list if f.strip()):  # Good length
            feature_score += 2
        if any('warranty' in f.lower() for f in features_list):  # Trust signals
            feature_score += 2
        if any(product_data['occasion'] in f.lower() for f in features_list):  # Occasion integration
            feature_score += 2
        if any('usa' in f.lower() or 'quality' in f.lower() for f in features_list):  # Quality terms
            feature_score += 1
        scores['features_quality'] = min(feature_score, 10)
    
    # 3. Description Quality Analysis (Max 10 points)
    if description:
        word_count = len(description.split())
        desc_score = 0
        if word_count >= 150 and word_count <= 400:  # Optimal length
            desc_score += 3
        if description.count('.') >= 5:  # Good structure
            desc_score += 2
        if any(word in description.lower() for word in ['better', 'superior', 'compared']):  # Comparisons
            desc_score += 2
        if product_data['occasion'] in description.lower():  # Occasion integration
            desc_score += 2
        if any(word in description.lower() for word in ['quality', 'warranty', 'guarantee']):  # Trust
            desc_score += 1
        scores['description_quality'] = min(desc_score, 10)
    
    # 4. Keywords Quality Analysis (Max 10 points)
    if keywords:
        keyword_list = keywords.split(',') if isinstance(keywords, str) else keywords
        keyword_score = 0
        if len(keyword_list) >= 15:  # Good quantity
            keyword_score += 3
        if any(product_data['occasion'] in k.lower() for k in keyword_list):  # Occasion keywords
            keyword_score += 2
        if any(marketplace.split('_')[0] in k.lower() for k in keyword_list):  # Platform-specific
            keyword_score += 2
        if any(word in keywords.lower() for word in ['best', 'top', 'premium', 'quality']):  # Power keywords
            keyword_score += 2
        if any(word in keywords.lower() for word in ['deal', 'special', 'exclusive']):  # Value keywords
            keyword_score += 1
        scores['keywords_quality'] = min(keyword_score, 10)
    
    # 5. Marketplace Optimization (Max 10 points)
    marketplace_score = 0
    full_content = f"{title} {features} {description} {keywords}".lower()
    
    if marketplace == 'walmart_usa':
        marketplace_terms = ['walmart', 'pickup', 'rollback', 'everyday low price', 'great value', 'price match']
    elif marketplace == 'walmart_canada':
        marketplace_terms = ['walmart', 'pickup', 'canadian', 'coast to coast', 'bilingual']
    elif marketplace == 'walmart_mexico':
        marketplace_terms = ['walmart', 'méxico', 'mexicana', 'familia', 'calidad']
    else:  # Amazon markets
        marketplace_terms = ['amazon', 'prime', 'shipping', 'delivery', 'reviews']
    
    marketplace_score += sum(1 for term in marketplace_terms if term in full_content)
    marketplace_score = min(marketplace_score, 10)
    scores['marketplace_optimization'] = marketplace_score
    
    # 6. Occasion Integration (Max 10 points)
    occasion_score = 0
    occasion = product_data['occasion'].lower()
    if occasion in full_content:
        occasion_score += 3
    if f"{occasion} gift" in full_content:
        occasion_score += 2
    if f"{occasion} special" in full_content:
        occasion_score += 2
    if f"{occasion} deal" in full_content:
        occasion_score += 3
    scores['occasion_integration'] = min(occasion_score, 10)
    
    # 7. Brand Tone Alignment (Max 10 points)
    brand_tone = product_data['brand_tone']
    tone_score = 0
    if brand_tone == 'luxury' and any(word in full_content for word in ['premium', 'luxury', 'sophisticated', 'exclusive']):
        tone_score += 5
    elif brand_tone == 'professional' and any(word in full_content for word in ['professional', 'certified', 'expert', 'precision']):
        tone_score += 5
    elif brand_tone == 'casual' and any(word in full_content for word in ['easy', 'simple', 'friendly', 'convenient']):
        tone_score += 5
    if product_data['brand_name'].lower() in full_content:
        tone_score += 3
    if any(word in full_content for word in ['trusted', 'reliable', 'quality']):
        tone_score += 2
    scores['brand_tone_alignment'] = min(tone_score, 10)
    
    # 8. Cultural Localization (Max 10 points)
    cultural_score = 0
    if 'usa' in marketplace:
        cultural_terms = ['american', 'usa', 'family', 'tradition', 'freedom', 'quality']
    elif 'canada' in marketplace:
        cultural_terms = ['canadian', 'coast to coast', 'bilingual', 'quality', 'eh', 'maple']
    elif 'mexico' in marketplace:
        cultural_terms = ['mexicana', 'familia', 'tradición', 'calidad', 'hogar']
    else:  # International Amazon
        cultural_terms = ['quality', 'premium', 'international', 'global', 'certified']
    
    cultural_score += sum(1 for term in cultural_terms if term in full_content)
    scores['cultural_localization'] = min(cultural_score, 10)
    
    # Calculate overall score
    overall_score = sum(scores.values()) / len(scores)
    scores['overall_score'] = overall_score
    
    return scores

def test_all_markets_comprehensive():
    """Test all major marketplaces for 10/10 quality achievement"""
    
    print("🌍 COMPREHENSIVE ALL MARKETS QUALITY TEST 🌍")
    print("=" * 65)
    
    # Create test user
    user, created = User.objects.get_or_create(username='all_markets_test')
    
    # Test markets to evaluate
    test_markets = [
        {'marketplace': 'walmart_usa', 'language': 'en-us', 'platform': 'walmart'},
        {'marketplace': 'walmart_canada', 'language': 'en-ca', 'platform': 'walmart'},
        {'marketplace': 'walmart_mexico', 'language': 'es-mx', 'platform': 'walmart'},
        {'marketplace': 'uk', 'language': 'en-gb', 'platform': 'amazon'},
        {'marketplace': 'au', 'language': 'en-au', 'platform': 'amazon'},
        {'marketplace': 'sg', 'language': 'en-sg', 'platform': 'amazon'},
        {'marketplace': 'be', 'language': 'nl-be', 'platform': 'amazon'},
        {'marketplace': 'tr', 'language': 'tr-tr', 'platform': 'amazon'},
        {'marketplace': 'pl', 'language': 'pl-pl', 'platform': 'amazon'},
        {'marketplace': 'eg', 'language': 'ar-eg', 'platform': 'amazon'},
        {'marketplace': 'in', 'language': 'en-in', 'platform': 'amazon'},
    ]
    
    # Test product for consistent evaluation
    test_product_data = {
        'name': 'Kitchen Knife Sharpener',
        'brand_name': 'ChefPro',
        'categories': 'Kitchen > Tools > Sharpeners',
        'price': 39.99,
        'occasion': 'christmas',
        'brand_tone': 'professional',
        'description': 'Professional knife sharpening system for home chefs',
        'features': 'Diamond Disc\nCeramic Disc\nAngle Guide\n2-Year Warranty\nEasy Setup'
    }
    
    service = ListingGeneratorService()
    all_results = {}
    
    for market_info in test_markets:
        marketplace = market_info['marketplace']
        language = market_info['language']
        platform = market_info['platform']
        
        print(f"\n🔍 TESTING MARKET: {marketplace.upper()}")
        print(f"   Language: {language}")
        print(f"   Platform: {platform}")
        
        # Create product for this market
        product_data = test_product_data.copy()
        product_data['marketplace'] = marketplace
        product_data['marketplace_language'] = language
        
        product = Product.objects.create(user=user, **product_data)
        
        try:
            # Generate listing for this market
            listing = service.generate_listing(product.id, platform)
            
            # Analyze quality
            analysis = analyze_listing_quality(listing, product_data, marketplace)
            
            all_results[marketplace] = {
                'listing': listing,
                'analysis': analysis,
                'success': True
            }
            
            print(f"   ✅ Status: {listing.status}")
            print(f"   🏆 Quality Score: {analysis['overall_score']:.1f}/10")
            
            # Show specific scores
            if analysis['overall_score'] >= 9.0:
                print(f"   🎉 EXCELLENT: Beats competitor standards!")
            elif analysis['overall_score'] >= 8.0:
                print(f"   ✅ VERY GOOD: Matches competitor quality")
            elif analysis['overall_score'] >= 7.0:
                print(f"   ⚠️ GOOD: Above average, room for improvement")
            else:
                print(f"   ❌ NEEDS WORK: Below competitor standards")
            
        except Exception as e:
            print(f"   ❌ Generation failed: {e}")
            all_results[marketplace] = {
                'listing': None,
                'analysis': {'overall_score': 0, 'error': str(e)},
                'success': False
            }
        
        finally:
            # Clean up
            product.delete()
    
    # Generate comprehensive report
    generate_all_markets_report(all_results)
    
    return all_results

def generate_all_markets_report(results):
    """Generate detailed quality report for all markets"""
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'all_markets_quality_report_{timestamp}.md'
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("# ALL MARKETS COMPREHENSIVE QUALITY REPORT\n\n")
        f.write(f"**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## EXECUTIVE SUMMARY\n\n")
        
        # Calculate statistics
        successful_markets = [k for k, v in results.items() if v['success']]
        failed_markets = [k for k, v in results.items() if not v['success']]
        
        if successful_markets:
            avg_score = sum(results[k]['analysis']['overall_score'] for k in successful_markets) / len(successful_markets)
            
            f.write(f"**Markets Tested:** {len(results)}\n")
            f.write(f"**Successful Generations:** {len(successful_markets)}\n")
            f.write(f"**Failed Generations:** {len(failed_markets)}\n")
            f.write(f"**Average Quality Score:** {avg_score:.1f}/10\n\n")
            
            # Count markets by quality tier
            excellent = sum(1 for k in successful_markets if results[k]['analysis']['overall_score'] >= 9.0)
            very_good = sum(1 for k in successful_markets if 8.0 <= results[k]['analysis']['overall_score'] < 9.0)
            good = sum(1 for k in successful_markets if 7.0 <= results[k]['analysis']['overall_score'] < 8.0)
            needs_work = sum(1 for k in successful_markets if results[k]['analysis']['overall_score'] < 7.0)
            
            f.write(f"**🎉 EXCELLENT (9.0+):** {excellent} markets\n")
            f.write(f"**✅ VERY GOOD (8.0-8.9):** {very_good} markets\n")
            f.write(f"**⚠️ GOOD (7.0-7.9):** {good} markets\n")
            f.write(f"**❌ NEEDS WORK (<7.0):** {needs_work} markets\n\n")
        
        f.write("## DETAILED ANALYSIS BY MARKET\n\n")
        
        # Sort by quality score (successful ones first)
        sorted_markets = sorted(results.items(), key=lambda x: x[1]['analysis']['overall_score'], reverse=True)
        
        for i, (marketplace, result) in enumerate(sorted_markets, 1):
            f.write(f"### {i}. {marketplace.upper()}\n\n")
            
            if result['success']:
                analysis = result['analysis']
                f.write(f"**Overall Score:** {analysis['overall_score']:.1f}/10\n\n")
                
                f.write("**Quality Breakdown:**\n")
                quality_metrics = [
                    ('Title Quality', 'title_quality'),
                    ('Features Quality', 'features_quality'),
                    ('Description Quality', 'description_quality'),
                    ('Keywords Quality', 'keywords_quality'),
                    ('Marketplace Optimization', 'marketplace_optimization'),
                    ('Occasion Integration', 'occasion_integration'),
                    ('Brand Tone Alignment', 'brand_tone_alignment'),
                    ('Cultural Localization', 'cultural_localization')
                ]
                
                for metric_name, metric_key in quality_metrics:
                    score = analysis.get(metric_key, 0)
                    status = "🟢" if score >= 8 else "🟡" if score >= 6 else "🔴"
                    f.write(f"- {status} {metric_name}: {score:.1f}/10\n")
                
                f.write(f"\n**Success Status:** {'✅ Generated successfully' if result['success'] else '❌ Generation failed'}\n\n")
                
            else:
                f.write(f"❌ **Generation Failed:** {result['analysis'].get('error', 'Unknown error')}\n\n")
        
        f.write("## OPTIMIZATION PRIORITIES\n\n")
        
        # Identify common weak areas
        if successful_markets:
            metric_averages = {}
            for metric in ['title_quality', 'features_quality', 'description_quality', 'keywords_quality', 
                          'marketplace_optimization', 'occasion_integration', 'brand_tone_alignment', 'cultural_localization']:
                avg = sum(results[k]['analysis'][metric] for k in successful_markets) / len(successful_markets)
                metric_averages[metric] = avg
            
            # Sort by lowest scores (biggest improvement opportunities)
            sorted_metrics = sorted(metric_averages.items(), key=lambda x: x[1])
            
            f.write("**Biggest Improvement Opportunities:**\n")
            for metric, avg_score in sorted_metrics[:3]:
                metric_name = metric.replace('_', ' ').title()
                f.write(f"1. **{metric_name}**: {avg_score:.1f}/10 average\n")
            
            f.write(f"\n**Strongest Areas:**\n")
            for metric, avg_score in sorted_metrics[-3:]:
                metric_name = metric.replace('_', ' ').title()
                f.write(f"1. **{metric_name}**: {avg_score:.1f}/10 average\n")
        
        f.write(f"\n## NEXT STEPS\n\n")
        f.write(f"1. **Priority Focus:** Optimize markets scoring below 8.0/10\n")
        f.write(f"2. **Quick Wins:** Address common weak metrics across all markets\n")
        f.write(f"3. **Market-Specific:** Customize prompts for cultural localization\n")
        f.write(f"4. **Quality Gates:** Ensure all markets achieve minimum 8.0/10 before deployment\n\n")
        
        f.write("---\n")
        f.write("*Report generated by All Markets Quality Assessment Tool*\n")
    
    print(f"\n📊 COMPREHENSIVE REPORT GENERATED: {filename}")
    return filename

if __name__ == "__main__":
    print("Starting All Markets Comprehensive Quality Test...")
    results = test_all_markets_comprehensive()
    print(f"\n🏁 Test completed! Analyzed {len(results)} markets.")