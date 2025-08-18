#!/usr/bin/env python3
"""
Detailed analysis of the most recent Sweden listing
"""

import os
import sys
import django
import json

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.models import GeneratedListing

def analyze_latest_sweden_listing():
    """Analyze the latest Sweden listing in detail"""
    
    print("DETAILED SWEDEN LISTING ANALYSIS")
    print("=" * 60)
    
    # Get the latest Sweden listing (ID 1051 from previous analysis)
    try:
        listing = GeneratedListing.objects.get(id=1051)
    except GeneratedListing.DoesNotExist:
        # Fall back to most recent Sweden listing
        listing = GeneratedListing.objects.filter(product__marketplace='se').order_by('-created_at').first()
    
    if not listing:
        print("No Sweden listing found!")
        return None
    
    print(f"Listing ID: {listing.id}")
    print(f"Product: {listing.product.name}")
    print(f"Marketplace: {listing.product.marketplace}")
    print(f"Language: {listing.product.marketplace_language}")
    print(f"Created: {listing.created_at}")
    
    analysis = {
        'listing_id': listing.id,
        'product_name': listing.product.name,
        'marketplace': listing.product.marketplace,
        'issues': [],
        'successes': [],
        'content_analysis': {},
        'overall_quality': 'Unknown'
    }
    
    # Analyze each component
    components = ['product_title', 'bullet_points', 'product_description', 'keywords', 'aplus_content_plan']
    
    for component in components:
        print(f"\n{component.upper()} ANALYSIS:")
        print("-" * 40)
        
        if hasattr(listing, component):
            content = getattr(listing, component)
            
            if content:
                # Convert to string for analysis
                if isinstance(content, list):
                    content_str = ' '.join(str(item) for item in content)
                    print(f"Count: {len(content)} items")
                else:
                    content_str = str(content)
                
                print(f"Length: {len(content_str)} characters")
                
                # Show sample content
                if len(content_str) > 300:
                    print(f"Content: {content_str[:300]}...")
                else:
                    print(f"Content: {content_str}")
                
                # Language analysis
                english_words = ['kitchen', 'knife', 'professional', 'quality', 'stainless', 'steel', 'the', 'and', 'with', 'for', 'is', 'experience', 'superior', 'premium', 'chair', 'gaming']
                swedish_words = ['kök', 'kniv', 'professionell', 'kvalitet', 'rostfritt', 'stål', 'och', 'med', 'för', 'är', 'bästa', 'premium', 'hög', 'set']
                
                english_count = sum(1 for word in english_words if word.lower() in content_str.lower())
                swedish_count = sum(1 for word in swedish_words if word.lower() in content_str.lower())
                
                print(f"English words detected: {english_count}")
                print(f"Swedish words detected: {swedish_count}")
                
                # Quality assessment for this component
                component_issues = []
                component_successes = []
                
                if component == 'product_title':
                    if len(content_str) < 50:
                        component_issues.append("Title too short")
                    elif len(content_str) > 200:
                        component_issues.append("Title too long")
                    else:
                        component_successes.append("Title length appropriate")
                
                if component == 'bullet_points':
                    if isinstance(content, list):
                        if len(content) < 3:
                            component_issues.append("Too few bullet points")
                        elif len(content) > 7:
                            component_issues.append("Too many bullet points")
                        else:
                            component_successes.append(f"Good number of bullets ({len(content)})")
                        
                        # Check individual bullets
                        for i, bullet in enumerate(content):
                            bullet_str = str(bullet)
                            if len(bullet_str) < 50:
                                component_issues.append(f"Bullet {i+1} too short")
                            elif len(bullet_str) > 300:
                                component_issues.append(f"Bullet {i+1} too long")
                
                if component == 'keywords':
                    if isinstance(content, list):
                        if len(content) < 10:
                            component_issues.append("Too few keywords")
                        elif len(content) > 50:
                            component_issues.append("Too many keywords")
                        else:
                            component_successes.append(f"Good keyword count ({len(content)})")
                    elif isinstance(content, str):
                        # If it's a string, count by splitting
                        keyword_list = [k.strip() for k in content.split(',') if k.strip()]
                        if len(keyword_list) < 10:
                            component_issues.append("Too few keywords")
                        else:
                            component_successes.append(f"Good keyword count ({len(keyword_list)})")
                
                # Language quality assessment
                if english_count > swedish_count and component != 'aplus_content_plan':
                    component_issues.append(f"More English ({english_count}) than Swedish ({swedish_count}) content")
                elif swedish_count > 0:
                    component_successes.append(f"Contains Swedish content ({swedish_count} words)")
                elif english_count == 0 and swedish_count == 0:
                    component_issues.append("No clear language markers found")
                
                # Store analysis
                analysis['content_analysis'][component] = {
                    'exists': True,
                    'length': len(content_str),
                    'english_words': english_count,
                    'swedish_words': swedish_count,
                    'issues': component_issues,
                    'successes': component_successes
                }
                
                analysis['issues'].extend(component_issues)
                analysis['successes'].extend(component_successes)
                
                print(f"Issues: {component_issues}")
                print(f"Successes: {component_successes}")
                
            else:
                print("Content: EMPTY")
                analysis['content_analysis'][component] = {
                    'exists': False,
                    'issues': ['Content is empty'],
                    'successes': []
                }
                analysis['issues'].append(f"{component} is empty")
        else:
            print("Field not found")
            analysis['content_analysis'][component] = {
                'exists': False,
                'issues': ['Field does not exist'],
                'successes': []
            }
            analysis['issues'].append(f"{component} field missing")
    
    # Overall quality assessment
    total_issues = len(analysis['issues'])
    total_successes = len(analysis['successes'])
    
    print(f"\nOVERALL ASSESSMENT:")
    print("=" * 40)
    print(f"Total Issues: {total_issues}")
    print(f"Total Successes: {total_successes}")
    
    if total_issues == 0:
        analysis['overall_quality'] = 'Excellent (10/10)'
    elif total_issues <= 3:
        analysis['overall_quality'] = 'Good (7-9/10)'
    elif total_issues <= 7:
        analysis['overall_quality'] = 'Fair (4-6/10)'
    else:
        analysis['overall_quality'] = 'Poor (1-3/10)'
    
    print(f"Overall Quality: {analysis['overall_quality']}")
    
    # Critical Issues Summary
    critical_issues = []
    if any('English' in issue and 'Swedish' in issue for issue in analysis['issues']):
        critical_issues.append("LANGUAGE MISMATCH: English content in Swedish marketplace")
    if any('empty' in issue.lower() for issue in analysis['issues']):
        critical_issues.append("MISSING CONTENT: Key fields are empty")
    if total_issues > 10:
        critical_issues.append("SYSTEM FAILURE: Too many issues detected")
    
    if critical_issues:
        print(f"\nCRITICAL ISSUES:")
        for issue in critical_issues:
            print(f"  🚨 {issue}")
    
    # What's Working vs What's Broken
    print(f"\nWHAT'S WORKING:")
    if analysis['successes']:
        for success in analysis['successes'][:5]:  # Top 5
            print(f"  ✅ {success}")
    else:
        print("  ❌ Nothing is working properly")
    
    print(f"\nWHAT'S BROKEN:")
    if analysis['issues']:
        for issue in analysis['issues'][:10]:  # Top 10
            print(f"  ❌ {issue}")
    else:
        print("  ✅ No issues detected")
    
    # Sweden-specific Analysis
    print(f"\nSWEDEN-SPECIFIC ANALYSIS:")
    print("-" * 40)
    
    swedish_quality_indicators = {
        'proper_language': any('Swedish content' in success for success in analysis['successes']),
        'no_english_contamination': not any('English' in issue and 'Swedish' in issue for issue in analysis['issues']),
        'complete_content': not any('empty' in issue.lower() for issue in analysis['issues']),
        'appropriate_length': not any('too short' in issue.lower() or 'too long' in issue.lower() for issue in analysis['issues'])
    }
    
    sweden_score = sum(swedish_quality_indicators.values())
    sweden_total = len(swedish_quality_indicators)
    
    print(f"Sweden Localization Score: {sweden_score}/{sweden_total}")
    for indicator, passed in swedish_quality_indicators.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {indicator}: {status}")
    
    if sweden_score == sweden_total:
        print("🇸🇪 SWEDEN QUALITY: EXCELLENT - Proper localization")
    elif sweden_score >= sweden_total * 0.7:
        print("🇸🇪 SWEDEN QUALITY: GOOD - Minor localization issues")
    else:
        print("🇸🇪 SWEDEN QUALITY: POOR - Major localization problems")
    
    return analysis

def main():
    """Main analysis function"""
    try:
        analysis = analyze_latest_sweden_listing()
        
        if analysis:
            # Save detailed analysis
            timestamp = listing.created_at.strftime("%Y%m%d_%H%M%S") if 'listing' in locals() else "unknown"
            filename = f"detailed_sweden_analysis_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"\n💾 Detailed analysis saved to: {filename}")
            
            return analysis
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = main()