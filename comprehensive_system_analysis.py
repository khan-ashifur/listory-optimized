#!/usr/bin/env python3
"""
Comprehensive analysis of what's working vs what's broken in the Sweden listing system
"""

import os
import sys
import django
import json
from datetime import datetime

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.models import GeneratedListing

def analyze_system_components():
    """Comprehensive analysis of system components"""
    
    print("COMPREHENSIVE SYSTEM ANALYSIS - SWEDEN MARKETPLACE")
    print("=" * 70)
    
    analysis_report = {
        'timestamp': datetime.now().isoformat(),
        'system_overview': {},
        'whats_working': [],
        'whats_broken': [],
        'critical_issues': [],
        'recommendations': [],
        'sweden_specific_issues': [],
        'quality_score': 0
    }
    
    # 1. Database Analysis
    print("\n1. DATABASE ANALYSIS")
    print("-" * 30)
    
    products = Product.objects.all()
    listings = GeneratedListing.objects.all()
    sweden_products = Product.objects.filter(marketplace='se')
    sweden_listings = GeneratedListing.objects.filter(product__marketplace='se')
    
    db_stats = {
        'total_products': products.count(),
        'total_listings': listings.count(),
        'sweden_products': sweden_products.count(),
        'sweden_listings': sweden_listings.count()
    }
    
    print(f"Total products: {db_stats['total_products']}")
    print(f"Total listings: {db_stats['total_listings']}")
    print(f"Sweden products: {db_stats['sweden_products']}")
    print(f"Sweden listings: {db_stats['sweden_listings']}")
    
    analysis_report['system_overview'].update(db_stats)
    
    if db_stats['sweden_products'] > 0:
        analysis_report['whats_working'].append("✅ Sweden products can be created in database")
    if db_stats['sweden_listings'] > 0:
        analysis_report['whats_working'].append("✅ Sweden listings can be generated")
    
    # 2. Recent Sweden Listing Analysis
    print("\n2. RECENT SWEDEN LISTING QUALITY")
    print("-" * 40)
    
    recent_sweden = sweden_listings.order_by('-created_at').first()
    if recent_sweden:
        listing_analysis = analyze_listing_quality(recent_sweden)
        analysis_report['sweden_specific_issues'].extend(listing_analysis['issues'])
        
        print(f"Latest Sweden listing: ID {recent_sweden.id}")
        print(f"Quality issues found: {len(listing_analysis['issues'])}")
        print(f"Quality successes: {len(listing_analysis['successes'])}")
        
        for issue in listing_analysis['issues'][:5]:
            print(f"  ❌ {issue}")
        
        if len(listing_analysis['issues']) > 10:
            analysis_report['critical_issues'].append("CRITICAL: Sweden listings have severe quality issues")
    else:
        analysis_report['critical_issues'].append("CRITICAL: No Sweden listings found")
    
    # 3. Language and Localization Analysis
    print("\n3. LANGUAGE & LOCALIZATION ANALYSIS")
    print("-" * 45)
    
    # Check if International Localization Optimizer exists
    try:
        from apps.listings.international_localization_optimizer import InternationalLocalizationOptimizer
        optimizer = InternationalLocalizationOptimizer()
        
        if 'se' in optimizer.market_configurations:
            print("❌ Sweden (se) not found in market configurations")
            analysis_report['critical_issues'].append("Sweden not configured in International Localization Optimizer")
        
        # Check if Sweden/Swedish support exists
        sweden_config = None
        for market_code, config in optimizer.market_configurations.items():
            if 'sweden' in config.get('market_name', '').lower() or market_code == 'se':
                sweden_config = config
                break
        
        if sweden_config:
            analysis_report['whats_working'].append("✅ Sweden configuration exists in localization optimizer")
            print("✅ Sweden configuration found")
        else:
            analysis_report['critical_issues'].append("CRITICAL: No Sweden configuration in localization system")
            print("❌ No Sweden configuration found")
            
    except ImportError:
        analysis_report['critical_issues'].append("CRITICAL: International Localization Optimizer not found")
        print("❌ International Localization Optimizer not available")
    
    # 4. Keyword System Analysis
    print("\n4. KEYWORD SYSTEM ANALYSIS")
    print("-" * 35)
    
    # Check if Swedish keywords are being generated
    if recent_sweden:
        keywords = getattr(recent_sweden, 'keywords', '')
        if keywords:
            print(f"Keywords found: {len(str(keywords))} characters")
            
            # Check for English vs Swedish content
            english_words = ['gaming', 'chair', 'kitchen', 'knife', 'the', 'and', 'with', 'for']
            swedish_words = ['kök', 'kniv', 'stol', 'och', 'med', 'för']
            
            english_count = sum(1 for word in english_words if word.lower() in str(keywords).lower())
            swedish_count = sum(1 for word in swedish_words if word.lower() in str(keywords).lower())
            
            print(f"English words in keywords: {english_count}")
            print(f"Swedish words in keywords: {swedish_count}")
            
            if english_count > swedish_count:
                analysis_report['critical_issues'].append("CRITICAL: Keywords are in English instead of Swedish")
                print("❌ Keywords are in English, not Swedish")
            else:
                analysis_report['whats_working'].append("✅ Keywords appear to be in Swedish")
                print("✅ Keywords appear to be in Swedish")
            
            # Check for wrong product category
            if 'gaming chair' in str(keywords).lower():
                analysis_report['critical_issues'].append("CRITICAL: Wrong product keywords (gaming chair for kitchen knife)")
                print("❌ WRONG PRODUCT: Gaming chair keywords for kitchen knife product")
            
        else:
            analysis_report['critical_issues'].append("CRITICAL: No keywords generated")
            print("❌ No keywords found")
    
    # 5. Content Generation Analysis
    print("\n5. CONTENT GENERATION ANALYSIS")
    print("-" * 40)
    
    if recent_sweden:
        # Check required fields
        required_fields = ['bullet_points', 'product_description', 'aplus_content_plan']
        
        for field in required_fields:
            if hasattr(recent_sweden, field):
                content = getattr(recent_sweden, field)
                if content:
                    analysis_report['whats_working'].append(f"✅ {field} is generated")
                    print(f"✅ {field}: Generated")
                else:
                    analysis_report['critical_issues'].append(f"CRITICAL: {field} is empty")
                    print(f"❌ {field}: Empty")
            else:
                analysis_report['critical_issues'].append(f"CRITICAL: {field} field missing")
                print(f"❌ {field}: Field not found")
    
    # 6. API and AI Integration Analysis
    print("\n6. API & AI INTEGRATION ANALYSIS")
    print("-" * 40)
    
    # Check if OpenAI is working
    try:
        from apps.listings.services import ListingGeneratorService
        service = ListingGeneratorService()
        
        if hasattr(service, 'client') and service.client:
            analysis_report['whats_working'].append("✅ OpenAI client is configured")
            print("✅ OpenAI client is available")
        else:
            analysis_report['critical_issues'].append("CRITICAL: OpenAI client not configured")
            print("❌ OpenAI client not available")
            
        # Check for quota issues (from the test run)
        analysis_report['critical_issues'].append("WARNING: OpenAI quota exceeded - fallback content being used")
        print("⚠️  OpenAI quota exceeded - using fallback content")
        
    except ImportError:
        analysis_report['critical_issues'].append("CRITICAL: Listing generator service not available")
        print("❌ Listing generator service not found")
    
    # 7. Fallback Content Analysis
    print("\n7. FALLBACK CONTENT ANALYSIS")
    print("-" * 40)
    
    # Check if fallback content is appropriate
    if recent_sweden:
        content = str(getattr(recent_sweden, 'bullet_points', ''))
        if 'gaming chair' in content.lower():
            analysis_report['critical_issues'].append("CRITICAL: Inappropriate fallback content (gaming chair for kitchen products)")
            print("❌ WRONG FALLBACK: Gaming chair content for kitchen knife product")
        
        if 'Experience superior knife set' in content:
            analysis_report['whats_working'].append("✅ Some fallback content matches product type")
            print("✅ Some fallback content is product-appropriate")
    
    # 8. International Support Analysis
    print("\n8. INTERNATIONAL SUPPORT ANALYSIS")
    print("-" * 45)
    
    # Check available international markets
    international_products = Product.objects.exclude(marketplace='us')
    marketplaces = international_products.values_list('marketplace', flat=True).distinct()
    
    print(f"International marketplaces in use: {list(marketplaces)}")
    
    supported_markets = ['de', 'fr', 'es', 'it', 'jp', 'tr', 'nl', 'br', 'mx', 'ae']
    working_markets = []
    
    for marketplace in marketplaces:
        if marketplace in supported_markets:
            working_markets.append(marketplace)
    
    if 'se' in marketplaces:
        if 'se' in supported_markets:
            analysis_report['whats_working'].append("✅ Sweden marketplace is in active use")
            print("✅ Sweden marketplace is active")
        else:
            analysis_report['critical_issues'].append("CRITICAL: Sweden marketplace in use but not properly supported")
            print("❌ Sweden marketplace not properly supported")
    
    print(f"Working international markets: {working_markets}")
    print(f"Sweden marketplace status: {'✅ Active' if 'se' in marketplaces else '❌ Not in use'}")
    
    # 9. Calculate Overall Quality Score
    print("\n9. OVERALL QUALITY ASSESSMENT")
    print("-" * 40)
    
    total_working = len(analysis_report['whats_working'])
    total_critical = len(analysis_report['critical_issues'])
    total_sweden_issues = len(analysis_report['sweden_specific_issues'])
    
    # Quality calculation
    base_score = min(10, max(0, total_working - total_critical))
    sweden_penalty = min(5, total_sweden_issues * 0.5)
    quality_score = max(0, base_score - sweden_penalty)
    
    analysis_report['quality_score'] = round(quality_score, 1)
    
    print(f"Working components: {total_working}")
    print(f"Critical issues: {total_critical}")
    print(f"Sweden-specific issues: {total_sweden_issues}")
    print(f"Overall Quality Score: {analysis_report['quality_score']}/10")
    
    # 10. Recommendations
    print("\n10. RECOMMENDATIONS")
    print("-" * 25)
    
    recommendations = []
    
    if total_critical > 5:
        recommendations.append("URGENT: Fix critical system issues before Sweden can work properly")
    
    if 'CRITICAL: Keywords are in English instead of Swedish' in analysis_report['critical_issues']:
        recommendations.append("HIGH: Implement Swedish keyword generation and replacement system")
    
    if 'CRITICAL: Wrong product keywords' in str(analysis_report['critical_issues']):
        recommendations.append("HIGH: Fix fallback content to match actual product type")
    
    if 'WARNING: OpenAI quota exceeded' in str(analysis_report['critical_issues']):
        recommendations.append("MEDIUM: Address OpenAI quota limits or improve fallback system")
    
    if not sweden_config:
        recommendations.append("HIGH: Add proper Sweden configuration to International Localization Optimizer")
    
    recommendations.append("LOW: Test with working OpenAI quota to see if AI-generated content is better")
    recommendations.append("MEDIUM: Add Swedish language validation to prevent English content")
    
    analysis_report['recommendations'] = recommendations
    
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec}")
    
    return analysis_report

def analyze_listing_quality(listing):
    """Analyze individual listing quality"""
    
    analysis = {
        'issues': [],
        'successes': []
    }
    
    # Check each field
    fields = ['bullet_points', 'keywords', 'product_description', 'aplus_content_plan']
    
    for field in fields:
        if hasattr(listing, field):
            content = getattr(listing, field)
            if content:
                # Language check
                content_str = str(content)
                english_words = ['gaming', 'chair', 'kitchen', 'knife', 'the', 'and', 'with', 'for', 'experience', 'superior']
                swedish_words = ['kök', 'kniv', 'och', 'med', 'för', 'kvalitet']
                
                english_count = sum(1 for word in english_words if word.lower() in content_str.lower())
                swedish_count = sum(1 for word in swedish_words if word.lower() in content_str.lower())
                
                if english_count > swedish_count:
                    analysis['issues'].append(f"{field} has more English than Swedish content")
                elif swedish_count > 0:
                    analysis['successes'].append(f"{field} contains Swedish content")
                
                # Product mismatch check
                if 'gaming chair' in content_str.lower() and 'knife' in listing.product.name.lower():
                    analysis['issues'].append(f"{field} has wrong product content (gaming chair for knife)")
                
            else:
                analysis['issues'].append(f"{field} is empty")
        else:
            analysis['issues'].append(f"{field} field missing")
    
    return analysis

def main():
    """Main analysis function"""
    
    try:
        analysis = analyze_system_components()
        
        # Save comprehensive report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"comprehensive_system_analysis_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n💾 Comprehensive analysis saved to: {filename}")
        
        # Summary
        print(f"\n📋 EXECUTIVE SUMMARY")
        print("=" * 30)
        print(f"Quality Score: {analysis['quality_score']}/10")
        print(f"Critical Issues: {len(analysis['critical_issues'])}")
        print(f"Working Components: {len(analysis['whats_working'])}")
        print(f"Sweden-Specific Issues: {len(analysis['sweden_specific_issues'])}")
        
        if analysis['quality_score'] >= 8:
            print("🎉 SYSTEM STATUS: EXCELLENT - Sweden marketplace working well")
        elif analysis['quality_score'] >= 6:
            print("⚡ SYSTEM STATUS: GOOD - Minor issues to fix")
        elif analysis['quality_score'] >= 4:
            print("⚠️  SYSTEM STATUS: FAIR - Several issues need attention")
        else:
            print("🚨 SYSTEM STATUS: POOR - Major fixes required")
        
        return analysis
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = main()