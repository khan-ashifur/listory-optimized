#!/usr/bin/env python3
"""
Test script for the new Occasion feature
Tests both Amazon and Walmart platforms with different occasions
"""

import requests
import json
import sys

def test_occasion_feature():
    """Test the occasion feature with Amazon and Walmart listings"""
    
    base_url = "http://localhost:8000/api"
    
    # Test cases with different occasions
    test_cases = [
        {
            "name": "Christmas Test",
            "data": {
                "name": "Wireless Bluetooth Headphones",
                "brand_name": "AudioTech", 
                "description": "Premium wireless headphones perfect for music lovers",
                "features": "Active noise cancellation\n30-hour battery\nComfortable ear cushions",
                "price": 79.99,
                "categories": "Electronics",
                "brand_tone": "professional",
                "occasion": "christmas"
            },
            "platforms": ["amazon", "walmart"]
        },
        {
            "name": "Valentine's Day Test", 
            "data": {
                "name": "Silk Rose Bouquet",
                "brand_name": "RomanceFloral", 
                "description": "Beautiful artificial roses that last forever, perfect romantic gift",
                "features": "Realistic silk petals\nLong-lasting beauty\nElegant presentation",
                "price": 39.99,
                "categories": "Home & Garden",
                "brand_tone": "luxury",
                "occasion": "valentines"
            },
            "platforms": ["amazon"]
        },
        {
            "name": "Custom Occasion Test",
            "data": {
                "name": "Personalized Photo Frame",
                "brand_name": "MemoryKeeper", 
                "description": "Custom wooden photo frame for special memories",
                "features": "Solid wood construction\nPersonalized engraving\nMultiple size options",
                "price": 24.99,
                "categories": "Home Decor",
                "brand_tone": "casual",
                "occasion": "Baby Shower"  # Custom occasion
            },
            "platforms": ["walmart"]
        }
    ]
    
    print("TESTING OCCASION FEATURE")
    print("=" * 60)
    
    results = []
    
    for test_case in test_cases:
        print(f"\n{test_case['name']}")
        print(f"   Occasion: {test_case['data']['occasion']}")
        print(f"   Platforms: {', '.join(test_case['platforms'])}")
        
        try:
            # Create product
            product_data = test_case['data'].copy()
            product_data["target_platform"] = test_case['platforms'][0]  # Use first platform for creation
            
            create_response = requests.post(
                f"{base_url}/core/products/",
                json=product_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if create_response.status_code in [200, 201]:
                product_data_result = create_response.json()
                product_id = product_data_result.get('id')
                print(f"   Product created: ID {product_id}")
                
                # Test each platform
                for platform in test_case['platforms']:
                    print(f"   Generating {platform} listing...")
                    
                    listing_response = requests.post(
                        f"{base_url}/listings/generate/{product_id}/{platform}/",
                        headers={"Content-Type": "application/json"},
                        timeout=60
                    )
                    
                    if listing_response.status_code in [200, 201]:
                        listing_data = listing_response.json()
                        listing_id = listing_data.get('id')
                        
                        # Check for occasion-specific content
                        occasion_found = check_occasion_content(listing_data, test_case['data']['occasion'], platform)
                        
                        results.append({
                            'test': test_case['name'],
                            'platform': platform,
                            'occasion': test_case['data']['occasion'],
                            'listing_id': listing_id,
                            'occasion_detected': occasion_found,
                            'status': 'PASS' if occasion_found else 'PARTIAL'
                        })
                        
                        print(f"   {platform} listing generated: ID {listing_id}")
                        if occasion_found:
                            print(f"   Occasion content detected!")
                        else:
                            print(f"   Occasion content not clearly detected")
                    else:
                        print(f"   {platform} listing failed: {listing_response.status_code}")
                        results.append({
                            'test': test_case['name'],
                            'platform': platform,
                            'occasion': test_case['data']['occasion'],
                            'status': 'FAILED'
                        })
            else:
                print(f"   Product creation failed: {create_response.status_code}")
                
        except Exception as e:
            print(f"   Test failed: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for r in results if r.get('status') == 'PASS')
    partial = sum(1 for r in results if r.get('status') == 'PARTIAL')
    failed = sum(1 for r in results if r.get('status') == 'FAILED')
    
    print(f"Fully Passed: {passed}")
    print(f"Partial Pass: {partial}")  
    print(f"Failed: {failed}")
    print(f"Success Rate: {((passed + partial) / len(results) * 100):.1f}%")
    
    print("\nDetailed Results:")
    for result in results:
        status_text = "PASS" if result['status'] == 'PASS' else "PARTIAL" if result['status'] == 'PARTIAL' else "FAIL"
        print(f"  {status_text} - {result['test']} - {result['platform']} - {result['occasion']}")
    
    return len(results) > 0 and failed == 0

def check_occasion_content(listing_data, occasion, platform):
    """Check if occasion-specific content is present in the listing"""
    
    occasion_keywords = {
        'christmas': ['christmas', 'holiday', 'gift', 'festive', 'xmas', 'seasonal'],
        'valentines': ['valentine', 'love', 'romantic', 'romance', 'heart', 'couple'],
        'mothers_day': ['mother', 'mom', 'maternal', 'caring', 'appreciation'],
        'fathers_day': ['father', 'dad', 'paternal', 'masculine', 'appreciation'],
        'halloween': ['halloween', 'spooky', 'costume', 'trick', 'treat'],
        'birthday': ['birthday', 'celebration', 'party', 'special day'],
        'graduation': ['graduation', 'achievement', 'success', 'milestone'],
        'wedding': ['wedding', 'marriage', 'bride', 'groom', 'ceremony']
    }
    
    # Get relevant keywords for this occasion
    keywords = occasion_keywords.get(occasion.lower(), [occasion.lower()])
    
    # Fields to check based on platform
    if platform == 'amazon':
        fields_to_check = [
            listing_data.get('title', ''),
            listing_data.get('product_description', ''),
            ' '.join(listing_data.get('bullet_points', [])) if isinstance(listing_data.get('bullet_points'), list) else listing_data.get('bullet_points', ''),
            ' '.join(listing_data.get('seo_keywords', {}).get('primary', [])) if isinstance(listing_data.get('seo_keywords'), dict) else ''
        ]
    else:  # walmart
        fields_to_check = [
            listing_data.get('walmart_product_title', ''),
            listing_data.get('walmart_description', ''),
            listing_data.get('walmart_key_features', ''),
        ]
    
    # Check if any occasion keywords appear in the content
    content = ' '.join(fields_to_check).lower()
    
    found_keywords = [keyword for keyword in keywords if keyword in content]
    
    return len(found_keywords) > 0

if __name__ == "__main__":
    success = test_occasion_feature()
    if success:
        print("\nOCCASION FEATURE TEST COMPLETED")
        sys.exit(0)
    else:
        print("\nOCCASION FEATURE TEST HAD ISSUES")
        sys.exit(1)