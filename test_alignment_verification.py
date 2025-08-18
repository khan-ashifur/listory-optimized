#!/usr/bin/env python3

"""
Verification Test: Check if Turkey and Mexico A+ content are now aligned
Test the fixes applied to services.py
"""

import os
import sys
import django
import re

# Django setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from django.contrib.auth.models import User

def extract_image_strategies(html_content):
    """Extract image strategy sections"""
    pattern = r'<strong class="text-gray-900">(?:Image Strategy|Görsel Strateji)</strong>\s*</div>\s*<p class="text-gray-600">(.*?)</p>'
    strategies = re.findall(pattern, html_content, re.DOTALL)
    return [s.strip() for s in strategies]

def test_alignment_verification():
    """Test if Turkey and Mexico now have aligned A+ content design"""
    print("TURKEY vs MEXICO A+ ALIGNMENT VERIFICATION TEST")
    print("=" * 60)
    print("Testing fixes applied to services.py...")
    
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username='alignment_verification_test')
    
    # Test product data
    product_data = {
        'brand_name': "TechPro",
        'description': "Premium wireless headphones with advanced noise cancellation and 40+ language translation",
        'price': 199.99,
        'categories': "Electronics/Audio/Headphones",
        'occasion': "general"
    }
    
    results = {}
    
    # Test markets
    markets = [
        {'code': 'mx', 'name': 'Mexico', 'product_name': 'Audífonos TechPro Premium'},
        {'code': 'tr', 'name': 'Turkey', 'product_name': 'TechPro Premium Kulaklık'}
    ]
    
    for market in markets:
        print(f"\nTesting {market['name']} ({market['code']})...")
        
        # Create product
        product = Product.objects.create(
            user=test_user,
            name=market['product_name'],
            marketplace=market['code'],
            marketplace_language=market['code'],
            **product_data
        )
        
        try:
            result = service.generate_listing(product_id=product.id, platform='amazon')
            
            if result and result.amazon_aplus_content:
                aplus_content = result.amazon_aplus_content
                
                # Extract image strategies
                image_strategies = extract_image_strategies(aplus_content)
                
                results[market['code']] = {
                    'content_length': len(aplus_content),
                    'image_strategies': image_strategies,
                    'english_prefixed': sum(1 for img in image_strategies if 'ENGLISH:' in img),
                    'total_strategies': len(image_strategies)
                }
                
                print(f"  Generated A+ content: {len(aplus_content)} characters")
                print(f"  Image strategies found: {len(image_strategies)}")
                print(f"  With ENGLISH prefix: {results[market['code']]['english_prefixed']}")
                
                # Show sample strategies
                print(f"  Sample strategies:")
                for i, strategy in enumerate(image_strategies[:2], 1):
                    prefix = "ENGLISH:" if 'ENGLISH:' in strategy else "NO PREFIX"
                    print(f"    {i}. [{prefix}] {strategy[:60]}...")
                
            else:
                print(f"  Failed to generate A+ content")
                results[market['code']] = {'error': 'No content generated'}
                
        except Exception as e:
            print(f"  Error: {str(e)}")
            results[market['code']] = {'error': str(e)}
        
        # Cleanup
        product.delete()
    
    # Comparison
    print(f"\nALIGNMENT VERIFICATION RESULTS")
    print("=" * 60)
    
    if 'tr' in results and 'mx' in results:
        tr_data = results['tr']
        mx_data = results['mx']
        
        if 'error' not in tr_data and 'error' not in mx_data:
            print(f"Mexico:")
            print(f"  Content length: {mx_data['content_length']}")
            print(f"  Image strategies: {mx_data['total_strategies']}")
            print(f"  With ENGLISH prefix: {mx_data['english_prefixed']}")
            
            print(f"\nTurkey:")
            print(f"  Content length: {tr_data['content_length']}")
            print(f"  Image strategies: {tr_data['total_strategies']}")
            print(f"  With ENGLISH prefix: {tr_data['english_prefixed']}")
            
            # Check alignment
            alignment_issues = []
            
            if mx_data['english_prefixed'] != tr_data['english_prefixed']:
                alignment_issues.append(f"ENGLISH prefix count differs: MX={mx_data['english_prefixed']} vs TR={tr_data['english_prefixed']}")
            
            if mx_data['total_strategies'] != tr_data['total_strategies']:
                alignment_issues.append(f"Strategy count differs: MX={mx_data['total_strategies']} vs TR={tr_data['total_strategies']}")
            
            content_diff = abs(mx_data['content_length'] - tr_data['content_length'])
            if content_diff > 1000:  # Allow 1000 char difference for language
                alignment_issues.append(f"Content length differs significantly: {content_diff} characters")
            
            print(f"\nALIGNMENT CHECK:")
            if not alignment_issues:
                print("  SUCCESS: Turkey and Mexico A+ content are now aligned!")
                print("  - Same number of image strategies")
                print("  - Same ENGLISH prefix count")
                print("  - Similar content length")
            else:
                print("  ISSUES FOUND:")
                for issue in alignment_issues:
                    print(f"    - {issue}")
        else:
            print("Could not verify alignment due to generation errors")
    
    return results

if __name__ == "__main__":
    test_alignment_verification()