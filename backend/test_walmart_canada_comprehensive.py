#!/usr/bin/env python
"""
WALMART CANADA COMPREHENSIVE QUALITY EVALUATION
==============================================

This script generates and evaluates Walmart Canada listings across multiple
product categories using the same 10/10 quality criteria that optimized Walmart USA.

Evaluation Criteria:
- Title: Brand-appropriate, no off-brand terms, clear value prop
- Features: Benefit-driven, unique claims, lifestyle hooks
- Description: Conversational tone, real-life use cases, not corporate
- Conversion: Urgency, social proof, clear CTAs
- SEO: Natural keywords, not overstuffed
- Attributes: Realistic pricing, proper compliance
- Rich Media: Relevant suggestions for Canadian market

Canadian-Specific Requirements:
- Bilingual considerations (English/French)
- Canadian pricing (CAD)
- Canadian cultural references
- Canadian compliance requirements
- Canadian shipping/warranty terms
"""

import os
import sys
import django
import json
from datetime import datetime

# Setup Django
backend_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.services import ListingGeneratorService
from apps.core.models import Product
from django.contrib.auth.models import User

def chatgpt_quality_evaluation(listing_data, product_data):
    """
    Evaluate listing quality using the same 10/10 criteria that optimized Walmart USA
    """
    
    evaluation = {
        'overall_score': 0,
        'category_scores': {},
        'issues': [],
        'strengths': [],
        'recommendations': []
    }
    
    # 1. TITLE EVALUATION (2 points)
    title = listing_data.get('product_title', '')
    title_score = 0
    
    # Title quality checks
    if len(title) >= 75 and len(title) <= 100:
        title_score += 0.5
        evaluation['strengths'].append("Title length optimal (75-100 chars)")
    else:
        evaluation['issues'].append(f"Title length suboptimal: {len(title)} chars (target: 75-100)")
    
    if product_data['brand_name'].lower() in title.lower():
        title_score += 0.5
        evaluation['strengths'].append("Brand name prominently featured in title")
    else:
        evaluation['issues'].append("Brand name not clearly featured in title")
    
    # Canadian specific title elements
    canadian_title_elements = ['canada', 'rollback', 'boxing day', 'walmart special', 'great value']
    canadian_count = sum(1 for element in canadian_title_elements if element.lower() in title.lower())
    if canadian_count >= 2:
        title_score += 0.5
        evaluation['strengths'].append(f"Strong Canadian market positioning ({canadian_count} elements)")
    else:
        evaluation['issues'].append("Insufficient Canadian market elements in title")
    
    # Value proposition clarity
    value_keywords = ['premium', 'professional', 'best', 'pro', 'special', 'rollback']
    if any(keyword.lower() in title.lower() for keyword in value_keywords):
        title_score += 0.5
        evaluation['strengths'].append("Clear value proposition in title")
    else:
        evaluation['issues'].append("Unclear value proposition in title")
    
    evaluation['category_scores']['title'] = title_score
    
    # 2. FEATURES EVALUATION (2 points) 
    features = listing_data.get('key_features', [])
    features_score = 0
    
    if len(features) >= 6:
        features_score += 0.5
        evaluation['strengths'].append(f"Adequate feature count ({len(features)} features)")
    else:
        evaluation['issues'].append(f"Insufficient features: {len(features)} (target: 6-7)")
    
    # Check for benefit-driven language vs technical specs
    benefit_keywords = ['enjoy', 'experience', 'perfect for', 'ideal', 'helps you', 'makes', 'ensures']
    benefit_count = sum(1 for feature in features for keyword in benefit_keywords if keyword.lower() in feature.lower())
    if benefit_count >= 3:
        features_score += 0.5
        evaluation['strengths'].append("Features focus on benefits over technical specs")
    else:
        evaluation['issues'].append("Features too technical, need more benefit-driven language")
    
    # Canadian compliance elements
    canadian_features = ['csa', 'health canada', 'canadian standards', 'coast to coast', 'bilingual']
    canadian_feature_count = sum(1 for feature in features for element in canadian_features if element.lower() in feature.lower())
    if canadian_feature_count >= 1:
        features_score += 0.5
        evaluation['strengths'].append("Canadian compliance/standards referenced")
    else:
        evaluation['issues'].append("Missing Canadian compliance references")
    
    # Walmart Canada integration
    walmart_elements = ['walmart', 'pickup', 'rollback', 'great value']
    walmart_feature_count = sum(1 for feature in features for element in walmart_elements if element.lower() in feature.lower())
    if walmart_feature_count >= 1 and walmart_feature_count <= 2:
        features_score += 0.5
        evaluation['strengths'].append("Appropriate Walmart Canada integration in features")
    else:
        evaluation['issues'].append("Suboptimal Walmart Canada integration (too much or too little)")
    
    evaluation['category_scores']['features'] = features_score
    
    # 3. DESCRIPTION EVALUATION (2 points)
    description = listing_data.get('product_description', '')
    description_score = 0
    
    # Word count check
    word_count = len(description.split())
    if 225 <= word_count <= 275:
        description_score += 0.5
        evaluation['strengths'].append(f"Description length optimal ({word_count} words)")
    else:
        evaluation['issues'].append(f"Description length suboptimal: {word_count} words (target: 225-275)")
    
    # Conversational vs corporate tone
    conversational_indicators = ['you', 'your', 'perfect for', 'imagine', 'whether', 'ideal for']
    corporate_indicators = ['utilize', 'leverage', 'facilitate', 'optimize', 'enhance productivity']
    
    conversational_count = sum(1 for indicator in conversational_indicators if indicator.lower() in description.lower())
    corporate_count = sum(1 for indicator in corporate_indicators if indicator.lower() in description.lower())
    
    if conversational_count > corporate_count:
        description_score += 0.5
        evaluation['strengths'].append("Conversational tone over corporate speak")
    else:
        evaluation['issues'].append("Too corporate, needs more conversational tone")
    
    # Canadian cultural references
    canadian_culture = ['canadian', 'coast to coast', 'cottage', 'winter', 'hockey', 'victoria day', 'canada day']
    canadian_culture_count = sum(1 for ref in canadian_culture if ref.lower() in description.lower())
    if canadian_culture_count >= 1:
        description_score += 0.5
        evaluation['strengths'].append("Canadian cultural references included")
    else:
        evaluation['issues'].append("Missing Canadian cultural connections")
    
    # Real-life use cases vs features list
    use_case_indicators = ['when you', 'perfect for', 'ideal for', 'whether you', 'great for']
    use_case_count = sum(1 for indicator in use_case_indicators if indicator.lower() in description.lower())
    if use_case_count >= 2:
        description_score += 0.5
        evaluation['strengths'].append("Real-life use cases presented")
    else:
        evaluation['issues'].append("Needs more real-life use case scenarios")
    
    evaluation['category_scores']['description'] = description_score
    
    # 4. CONVERSION OPTIMIZATION (2 points)
    conversion_score = 0
    
    # Urgency/scarcity elements
    urgency_terms = ['limited time', 'sale', 'rollback', 'special offer', 'while supplies last']
    urgency_count = sum(1 for term in urgency_terms if term.lower() in (title + ' ' + description).lower())
    if urgency_count >= 1:
        conversion_score += 0.5
        evaluation['strengths'].append("Urgency/scarcity elements present")
    else:
        evaluation['issues'].append("Missing urgency/scarcity elements")
    
    # Social proof elements  
    social_proof = ['customer favorite', 'best seller', 'highly rated', 'trusted by', 'preferred by']
    social_proof_count = sum(1 for proof in social_proof if proof.lower() in description.lower())
    if social_proof_count >= 1:
        conversion_score += 0.5
        evaluation['strengths'].append("Social proof elements included")
    else:
        evaluation['issues'].append("Missing social proof elements")
    
    # Clear value proposition
    value_props = ['best value', 'great price', 'unbeatable', 'compare', 'save', 'affordable']
    value_prop_count = sum(1 for prop in value_props if prop.lower() in (title + ' ' + description).lower())
    if value_prop_count >= 2:
        conversion_score += 0.5
        evaluation['strengths'].append("Clear value proposition communicated")
    else:
        evaluation['issues'].append("Value proposition needs strengthening")
    
    # Call-to-action strength
    cta_terms = ['order now', 'buy today', 'get yours', 'shop now', 'pickup today', 'free shipping']
    cta_count = sum(1 for cta in cta_terms if cta.lower() in description.lower())
    if cta_count >= 1:
        conversion_score += 0.5
        evaluation['strengths'].append("Call-to-action present")
    else:
        evaluation['issues'].append("Missing or weak call-to-action")
    
    evaluation['category_scores']['conversion'] = conversion_score
    
    # 5. SEO OPTIMIZATION (2 points)
    keywords = listing_data.get('seo_keywords', [])
    seo_score = 0
    
    # Keyword count and diversity
    if len(keywords) >= 20:
        seo_score += 0.5
        evaluation['strengths'].append(f"Adequate keyword count ({len(keywords)} keywords)")
    else:
        evaluation['issues'].append(f"Insufficient keywords: {len(keywords)} (target: 25+)")
    
    # Canadian market keywords
    canadian_seo = ['walmart canada', 'canada day', 'boxing day', 'pickup canada', 'rollback']
    canadian_seo_count = sum(1 for keyword in keywords for term in canadian_seo if term.lower() in keyword.lower())
    if canadian_seo_count >= 3:
        seo_score += 0.5
        evaluation['strengths'].append("Strong Canadian SEO targeting")
    else:
        evaluation['issues'].append("Insufficient Canadian market SEO keywords")
    
    # Natural vs stuffed keywords (check for repetition)
    keyword_text = ' '.join(keywords).lower()
    unique_words = set(keyword_text.split())
    total_words = len(keyword_text.split())
    if len(unique_words) / total_words > 0.6:  # More than 60% unique
        seo_score += 0.5
        evaluation['strengths'].append("Natural keyword distribution")
    else:
        evaluation['issues'].append("Keywords appear stuffed/repetitive")
    
    # Long-tail keyword presence
    long_tail_keywords = [kw for kw in keywords if len(kw.split()) >= 3]
    if len(long_tail_keywords) >= 5:
        seo_score += 0.5
        evaluation['strengths'].append(f"Good long-tail keyword strategy ({len(long_tail_keywords)} phrases)")
    else:
        evaluation['issues'].append("Need more long-tail keywords for better targeting")
    
    evaluation['category_scores']['seo'] = seo_score
    
    # Calculate overall score
    evaluation['overall_score'] = sum(evaluation['category_scores'].values())
    
    # Generate recommendations based on score
    if evaluation['overall_score'] >= 9.0:
        evaluation['quality_level'] = "EXCELLENT (10/10 ready)"
    elif evaluation['overall_score'] >= 7.5:
        evaluation['quality_level'] = "GOOD (Minor optimizations needed)"
    elif evaluation['overall_score'] >= 6.0:
        evaluation['quality_level'] = "FAIR (Moderate improvements required)"
    else:
        evaluation['quality_level'] = "POOR (Major overhaul needed)"
    
    return evaluation

def test_product_category(category_name, product_config):
    """Test a specific product category for Walmart Canada"""
    
    print(f"\n{'='*80}")
    print(f"🇨🇦 TESTING {category_name.upper()} - WALMART CANADA")
    print(f"{'='*80}")
    
    user, _ = User.objects.get_or_create(username='test_walmart_canada_comprehensive')
    
    # Create product
    product = Product.objects.create(
        user=user,
        **product_config
    )
    
    print(f"✅ Created {category_name} product:")
    for key, value in product_config.items():
        print(f"   {key}: {value}")
    
    try:
        # Generate listing
        service = ListingGeneratorService()
        listing = service.generate_listing(product.id, 'walmart')
        
        # Extract listing data for evaluation
        listing_data = {
            'product_title': listing.walmart_product_title,
            'key_features': listing.walmart_key_features.split('\n') if listing.walmart_key_features else [],
            'product_description': listing.walmart_description,
            'seo_keywords': listing.walmart_seo_keywords.split(', ') if listing.walmart_seo_keywords else []
        }
        
        # Perform quality evaluation
        evaluation = chatgpt_quality_evaluation(listing_data, product_config)
        
        print(f"\n📊 QUALITY EVALUATION RESULTS:")
        print(f"   Overall Score: {evaluation['overall_score']}/10.0")
        print(f"   Quality Level: {evaluation['quality_level']}")
        
        print(f"\n📈 CATEGORY BREAKDOWN:")
        for category, score in evaluation['category_scores'].items():
            print(f"   {category.title()}: {score}/2.0")
        
        print(f"\n✅ STRENGTHS ({len(evaluation['strengths'])}):")
        for strength in evaluation['strengths'][:5]:  # Show top 5
            print(f"   • {strength}")
        
        print(f"\n❌ ISSUES TO FIX ({len(evaluation['issues'])}):")
        for issue in evaluation['issues'][:5]:  # Show top 5
            print(f"   • {issue}")
        
        print(f"\n📋 LISTING PREVIEW:")
        print(f"   Title ({len(listing_data['product_title'])} chars): {listing_data['product_title']}")
        print(f"   Features: {len(listing_data['key_features'])} bullets")
        print(f"   Description: {len(listing_data['product_description'].split())} words")
        print(f"   SEO Keywords: {len(listing_data['seo_keywords'])} terms")
        
        # Canadian-specific elements check
        canadian_elements = []
        full_text = (listing_data['product_title'] + ' ' + 
                    ' '.join(listing_data['key_features']) + ' ' +
                    listing_data['product_description']).lower()
        
        if 'canada' in full_text: canadian_elements.append('Canada references')
        if 'rollback' in full_text: canadian_elements.append('Rollback pricing')
        if 'csa' in full_text: canadian_elements.append('CSA certification')
        if 'walmart' in full_text: canadian_elements.append('Walmart integration')
        if 'boxing day' in full_text: canadian_elements.append('Canadian occasions')
        if 'pickup' in full_text: canadian_elements.append('Pickup services')
        
        print(f"\n🇨🇦 CANADIAN MARKET ELEMENTS ({len(canadian_elements)}):")
        for element in canadian_elements:
            print(f"   ✓ {element}")
        
        print(f"\n🌐 Test URL: http://localhost:3000/results/{listing.id}")
        
        return {
            'category': category_name,
            'product_id': product.id,
            'listing_id': listing.id,
            'evaluation': evaluation,
            'listing_data': listing_data,
            'canadian_elements': canadian_elements
        }
        
    except Exception as e:
        print(f"❌ Error generating listing: {e}")
        import traceback
        traceback.print_exc()
        return None
    
    finally:
        # Clean up
        product.delete()

def generate_optimization_report(test_results):
    """Generate comprehensive optimization report for Walmart Canada"""
    
    print(f"\n{'='*100}")
    print(f"🇨🇦 WALMART CANADA OPTIMIZATION REPORT - {datetime.now().strftime('%Y%m%d_%H%M%S')}")
    print(f"{'='*100}")
    
    # Calculate overall statistics
    valid_results = [r for r in test_results if r is not None]
    if not valid_results:
        print("❌ No valid results to analyze")
        return
    
    avg_score = sum(r['evaluation']['overall_score'] for r in valid_results) / len(valid_results)
    scores = [r['evaluation']['overall_score'] for r in valid_results]
    
    print(f"\n📊 OVERALL PERFORMANCE:")
    print(f"   Categories Tested: {len(valid_results)}")
    print(f"   Average Score: {avg_score:.1f}/10.0")
    print(f"   Best Score: {max(scores):.1f}/10.0")
    print(f"   Worst Score: {min(scores):.1f}/10.0")
    
    # Category performance breakdown
    print(f"\n📈 CATEGORY PERFORMANCE:")
    category_scores = {}
    for result in valid_results:
        for category, score in result['evaluation']['category_scores'].items():
            if category not in category_scores:
                category_scores[category] = []
            category_scores[category].append(score)
    
    for category, scores in category_scores.items():
        avg_cat_score = sum(scores) / len(scores)
        print(f"   {category.title()}: {avg_cat_score:.1f}/2.0 (across {len(scores)} products)")
    
    # Most common issues
    all_issues = []
    for result in valid_results:
        all_issues.extend(result['evaluation']['issues'])
    
    issue_counts = {}
    for issue in all_issues:
        # Simplify issue for counting
        issue_key = issue.split(':')[0] if ':' in issue else issue
        issue_counts[issue_key] = issue_counts.get(issue_key, 0) + 1
    
    print(f"\n❌ TOP ISSUES TO FIX:")
    sorted_issues = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)
    for issue, count in sorted_issues[:5]:
        print(f"   {count}x: {issue}")
    
    # Canadian market integration analysis
    print(f"\n🇨🇦 CANADIAN MARKET INTEGRATION:")
    canadian_element_counts = {}
    for result in valid_results:
        for element in result['canadian_elements']:
            canadian_element_counts[element] = canadian_element_counts.get(element, 0) + 1
    
    for element, count in sorted(canadian_element_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(valid_results)) * 100
        print(f"   {percentage:.0f}% have: {element}")
    
    # Recommendations
    print(f"\n🎯 PRIORITY OPTIMIZATION RECOMMENDATIONS:")
    
    if avg_score < 8.0:
        print(f"   1. URGENT: Average score {avg_score:.1f}/10.0 needs improvement")
        
    # Title optimization
    title_scores = [sum(r['evaluation']['category_scores'].get('title', 0) for r in valid_results) / len(valid_results)]
    if title_scores[0] < 1.5:
        print(f"   2. TITLE: Improve title optimization (current: {title_scores[0]:.1f}/2.0)")
        
    # Features optimization  
    feature_scores = [sum(r['evaluation']['category_scores'].get('features', 0) for r in valid_results) / len(valid_results)]
    if feature_scores[0] < 1.5:
        print(f"   3. FEATURES: Enhance feature benefits focus (current: {feature_scores[0]:.1f}/2.0)")
        
    # Canadian integration
    canada_integration = sum(len(r['canadian_elements']) for r in valid_results) / len(valid_results)
    if canada_integration < 4:
        print(f"   4. CANADIAN INTEGRATION: Strengthen market elements (current: {canada_integration:.1f} elements avg)")
        
    # Conversion optimization
    conversion_scores = [sum(r['evaluation']['category_scores'].get('conversion', 0) for r in valid_results) / len(valid_results)]
    if conversion_scores[0] < 1.5:
        print(f"   5. CONVERSION: Add urgency and social proof (current: {conversion_scores[0]:.1f}/2.0)")
    
    print(f"\n💡 NEXT STEPS:")
    print(f"   1. Focus on categories scoring below 8.0/10.0")
    print(f"   2. Implement top 3 issue fixes across all categories")
    print(f"   3. Strengthen Canadian market positioning")
    print(f"   4. Test bilingual keyword integration")
    print(f"   5. Compare against Walmart USA optimized version for consistency")
    
    return {
        'avg_score': avg_score,
        'category_scores': category_scores,
        'top_issues': sorted_issues[:5],
        'canadian_integration': canadian_element_counts
    }

def main():
    """Main test execution for comprehensive Walmart Canada evaluation"""
    
    print("🇨🇦 WALMART CANADA COMPREHENSIVE QUALITY EVALUATION")
    print("=" * 55)
    print("Testing multiple product categories with 10/10 quality standards")
    print("Same criteria that optimized Walmart USA to 8.1/10")
    
    # Test product configurations for different categories
    test_products = [
        {
            'name': 'Kitchen Electronics - Stand Mixer',
            'config': {
                'name': 'Professional Stand Mixer 6Qt',
                'brand_name': 'KitchenMaster',
                'target_platform': 'walmart',
                'marketplace': 'walmart_canada',
                'marketplace_language': 'en-ca',
                'price': 299.99,
                'occasion': 'boxing_day',
                'brand_tone': 'professional',
                'categories': 'Home & Kitchen > Kitchen Appliances > Stand Mixers',
                'description': 'Professional 6-quart stand mixer with planetary mixing action and multiple speed settings',
                'features': '6-Quart Stainless Steel Bowl\nPlanetary Mixing Action\n10 Speed Settings\nDishwasher Safe Attachments\nCSA Certified for Canada\nTilt-Head Design'
            }
        },
        {
            'name': 'Electronics - Gaming Headset',
            'config': {
                'name': 'Wireless Gaming Headset Pro',
                'brand_name': 'GameForce',
                'target_platform': 'walmart',
                'marketplace': 'walmart_canada',
                'marketplace_language': 'en-ca',
                'price': 129.99,
                'occasion': 'canada_day',
                'brand_tone': 'trendy',
                'categories': 'Electronics > Gaming > Headsets',
                'description': 'Professional wireless gaming headset with 7.1 surround sound and noise cancellation',
                'features': '7.1 Surround Sound\nActive Noise Cancellation\n30-Hour Battery Life\nFast USB-C Charging\nCompatible with PC/PS5/Xbox\nDetachable Microphone'
            }
        },
        {
            'name': 'Home Goods - Air Purifier',
            'config': {
                'name': 'HEPA Air Purifier Large Room',
                'brand_name': 'CleanAir Pro',
                'target_platform': 'walmart',
                'marketplace': 'walmart_canada',
                'marketplace_language': 'en-ca',
                'price': 199.99,
                'occasion': 'winter_wellness',
                'brand_tone': 'health_conscious',
                'categories': 'Home & Garden > Air Quality > Air Purifiers',
                'description': 'Medical-grade HEPA air purifier for large rooms up to 1000 sq ft',
                'features': 'True HEPA H13 Filter\nCovers 1000 Sq Ft\nQuiet Operation 25dB\nSmart Air Quality Sensor\nHealth Canada Approved\nWiFi App Control'
            }
        },
        {
            'name': 'Personal Care - Electric Toothbrush',
            'config': {
                'name': 'Sonic Electric Toothbrush',
                'brand_name': 'DentalPro',
                'target_platform': 'walmart',
                'marketplace': 'walmart_canada',
                'marketplace_language': 'en-ca',
                'price': 89.99,
                'occasion': 'new_year_health',
                'brand_tone': 'health_conscious',
                'categories': 'Health & Personal Care > Oral Care > Electric Toothbrushes',
                'description': 'Advanced sonic electric toothbrush with multiple cleaning modes and pressure sensor',
                'features': 'Sonic Technology 40000 VPM\nPressure Sensor Protection\n5 Cleaning Modes\n4-Week Battery Life\nWaterproof IPX7 Rating\n2-Minute Timer'
            }
        },
        {
            'name': 'Fitness - Yoga Mat',
            'config': {
                'name': 'Premium Eco Yoga Mat',
                'brand_name': 'ZenFlow',
                'target_platform': 'walmart',
                'marketplace': 'walmart_canada',
                'marketplace_language': 'en-ca',
                'price': 49.99,
                'occasion': 'new_year_fitness',
                'brand_tone': 'wellness',
                'categories': 'Sports & Recreation > Fitness > Yoga',
                'description': 'Eco-friendly premium yoga mat with superior grip and cushioning',
                'features': 'Eco-Friendly TPE Material\nSuperior Grip Technology\n6mm Thick Cushioning\nAlignment Lines\nLightweight Portable\nNon-Slip Surface'
            }
        }
    ]
    
    # Execute tests
    test_results = []
    for product_test in test_products:
        result = test_product_category(product_test['name'], product_test['config'])
        test_results.append(result)
        
        # Brief pause between tests
        import time
        time.sleep(1)
    
    # Generate comprehensive report
    optimization_report = generate_optimization_report(test_results)
    
    print(f"\n🎯 WALMART CANADA EVALUATION COMPLETE!")
    print(f"📊 Ready for optimization implementation based on identified issues")
    print(f"🇺🇸 Compare against Walmart USA (8.1/10) for consistency improvements")

if __name__ == '__main__':
    main()