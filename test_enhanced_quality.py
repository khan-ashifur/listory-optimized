#!/usr/bin/env python
"""
TEST ENHANCED QUALITY
=====================

Test the enhanced services.py with quality improvements to verify 10/10 achievement.
"""

import os
import sys
import django
from datetime import datetime

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_path)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.services import ListingGeneratorService
from apps.core.models import Product
from django.contrib.auth.models import User

def test_enhanced_marketplace_quality():
    """Test enhanced marketplace quality improvements."""
    
    print("TESTING ENHANCED MARKETPLACE QUALITY")
    print("=" * 50)
    print("Testing Phase 1 improvements: Features, Description, Keywords")
    
    service = ListingGeneratorService()
    user, _ = User.objects.get_or_create(username='enhanced_quality_tester')
    
    # Test product for validation
    test_product = {
        'name': 'Professional Gaming Headset',
        'brand_name': 'AudioPro',
        'description': 'Professional wireless gaming headset with active noise cancellation',
        'categories': 'Electronics > Audio > Gaming Headphones',
        'features': 'Wireless 2.4GHz Connection\nActive Noise Cancellation\n50-Hour Battery Life\nErgonomic Over-Ear Design\nHigh-Fidelity Audio Drivers\nDetachable Boom Microphone',
        'price': 129.99,
        'occasion': 'christmas',
        'brand_tone': 'professional'
    }
    
    # Test priority markets
    test_markets = [
        ('walmart_usa', 'en-us', 'walmart'),
        ('us', 'en-us', 'amazon'),
        ('uk', 'en-gb', 'amazon')
    ]
    
    results = {}
    
    for marketplace, language, platform in test_markets:
        print(f"\nTesting {marketplace.upper()} with enhanced quality...")
        
        try:
            # Create product
            product = Product.objects.create(
                user=user,
                target_platform=platform,
                marketplace=marketplace,
                marketplace_language=language,
                **test_product
            )
            
            # Generate listing with enhancements
            listing = service.generate_listing(product.id, platform)
            
            if listing.status == 'completed':
                # Quick quality check
                if marketplace.startswith('walmart'):
                    title = getattr(listing, 'walmart_product_title', '')
                    features = getattr(listing, 'walmart_key_features', '')
                    description = getattr(listing, 'walmart_description', '')
                    keywords = getattr(listing, 'walmart_search_terms', '') or getattr(listing, 'keywords', '')
                else:
                    title = getattr(listing, 'title', '')
                    features = getattr(listing, 'bullet_points', '')
                    description = getattr(listing, 'long_description', '')
                    keywords = getattr(listing, 'amazon_keywords', '') or getattr(listing, 'keywords', '')
                
                # Calculate improvement indicators
                quality_indicators = {
                    'title_length': len(title) if title else 0,
                    'features_count': len([f for f in features.split('\n') if f.strip()]) if features else 0,
                    'description_words': len(description.split()) if description else 0,
                    'keywords_count': len([k for k in keywords.split(',') if k.strip()]) if keywords else 0,
                    'has_enhanced_language': any(word in (title + features + description).lower() for word in [
                        'professional', 'premium', 'superior', 'advanced', 'industry-leading', 
                        'engineered', 'experience', 'reliable', 'quality'
                    ]),
                    'has_benefit_language': any(phrase in (features + description).lower() for phrase in [
                        'delivers', 'ensures', 'provides', 'experience', 'enjoy', 'feel confident'
                    ]),
                    'has_emotional_hooks': any(phrase in description.lower() for phrase in [
                        'imagine', 'experience', 'feel', 'enjoy', 'love', 'peace of mind'
                    ])
                }
                
                results[marketplace] = {
                    'status': 'success',
                    'quality_indicators': quality_indicators,
                    'title_preview': title[:80] + '...' if len(title) > 80 else title,
                    'features_preview': features.split('\n')[0][:80] + '...' if features else 'No features',
                    'description_preview': description[:100] + '...' if len(description) > 100 else description
                }
                
                # Display results
                print(f"   Status: SUCCESS")
                print(f"   Title Length: {quality_indicators['title_length']} chars")
                print(f"   Features Count: {quality_indicators['features_count']}")
                print(f"   Description Words: {quality_indicators['description_words']}")
                print(f"   Keywords Count: {quality_indicators['keywords_count']}")
                print(f"   Enhanced Language: {'YES' if quality_indicators['has_enhanced_language'] else 'NO'}")
                print(f"   Benefit Language: {'YES' if quality_indicators['has_benefit_language'] else 'NO'}")
                print(f"   Emotional Hooks: {'YES' if quality_indicators['has_emotional_hooks'] else 'NO'}")
                
                # Show sample content
                print(f"   Title: {quality_indicators['title_length'] > 0}")
                print(f"   Features: {quality_indicators['features_count'] > 0}")
                print(f"   Description: {quality_indicators['description_words'] > 0}")
                
            else:
                print(f"   Status: FAILED - {listing.status}")
                results[marketplace] = {'status': 'failed', 'error': listing.status}
            
        except Exception as e:
            print(f"   Status: ERROR - {str(e)[:100]}")
            results[marketplace] = {'status': 'error', 'error': str(e)}
        finally:
            if 'product' in locals():
                try:
                    product.delete()
                except:
                    pass
    
    # Summary analysis
    print(f"\nENHANCEMENT VALIDATION SUMMARY:")
    print("=" * 40)
    
    successful_tests = [r for r in results.values() if r['status'] == 'success']
    
    if successful_tests:
        avg_title_length = sum(r['quality_indicators']['title_length'] for r in successful_tests) / len(successful_tests)
        avg_features_count = sum(r['quality_indicators']['features_count'] for r in successful_tests) / len(successful_tests)
        avg_description_words = sum(r['quality_indicators']['description_words'] for r in successful_tests) / len(successful_tests)
        avg_keywords_count = sum(r['quality_indicators']['keywords_count'] for r in successful_tests) / len(successful_tests)
        
        enhanced_language_pct = sum(1 for r in successful_tests if r['quality_indicators']['has_enhanced_language']) / len(successful_tests) * 100
        benefit_language_pct = sum(1 for r in successful_tests if r['quality_indicators']['has_benefit_language']) / len(successful_tests) * 100
        emotional_hooks_pct = sum(1 for r in successful_tests if r['quality_indicators']['has_emotional_hooks']) / len(successful_tests) * 100
        
        print(f"Successful Tests: {len(successful_tests)}/{len(test_markets)}")
        print(f"Average Title Length: {avg_title_length:.1f} chars")
        print(f"Average Features Count: {avg_features_count:.1f}")
        print(f"Average Description Words: {avg_description_words:.1f}")
        print(f"Average Keywords Count: {avg_keywords_count:.1f}")
        print(f"Enhanced Language: {enhanced_language_pct:.0f}% of tests")
        print(f"Benefit Language: {benefit_language_pct:.0f}% of tests")
        print(f"Emotional Hooks: {emotional_hooks_pct:.0f}% of tests")
        
        # Quality assessment
        quality_score = 0
        if avg_title_length >= 80: quality_score += 2
        if avg_features_count >= 5: quality_score += 2
        if avg_description_words >= 150: quality_score += 2
        if avg_keywords_count >= 15: quality_score += 2
        if enhanced_language_pct >= 90: quality_score += 1
        if benefit_language_pct >= 90: quality_score += 1
        
        print(f"\nENHANCEMENT QUALITY SCORE: {quality_score}/10")
        
        if quality_score >= 8:
            print("EXCELLENT - Enhancements working as expected!")
        elif quality_score >= 6:
            print("GOOD - Enhancements showing improvement")
        else:
            print("NEEDS WORK - Enhancements may not be fully active")
    
    # Save detailed results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'enhanced_quality_test_results_{timestamp}.json'
    
    import json
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed results saved: {filename}")
    return results

if __name__ == '__main__':
    test_enhanced_marketplace_quality()