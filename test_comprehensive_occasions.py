#!/usr/bin/env python3
"""
Comprehensive test for occasion handling analysis
Tests different scenarios and tone combinations
"""

import requests
import json
import sys

def test_comprehensive_occasions():
    """Test various occasion and tone combinations"""
    
    base_url = "http://localhost:8000/api"
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Christmas + Professional Tone",
            "data": {
                "name": "Wireless Noise-Cancelling Headphones",
                "brand_name": "AudioPro", 
                "description": "Premium wireless headphones with active noise cancellation technology",
                "features": "Active noise cancellation, 30-hour battery life, Quick charge, Premium materials",
                "price": 149.99,
                "categories": "Electronics, Audio",
                "brand_tone": "professional",
                "occasion": "Christmas",
                "target_keywords": "wireless headphones, noise cancelling, premium audio"
            }
        },
        {
            "name": "Valentine's Day + Luxury Tone",
            "data": {
                "name": "Silk Rose Bouquet with Crystal Vase",
                "brand_name": "EternalRomance", 
                "description": "Handcrafted silk roses arranged in a genuine crystal vase, perfect for expressing love",
                "features": "Handcrafted silk petals, Crystal vase included, Long-lasting beauty, Elegant presentation",
                "price": 89.99,
                "categories": "Home & Garden, Gifts",
                "brand_tone": "luxury",
                "occasion": "Valentine's Day",
                "target_keywords": "silk roses, romantic gift, valentine flowers"
            }
        },
        {
            "name": "Mother's Day + Casual Tone",
            "data": {
                "name": "Personalized Photo Collage Frame",
                "brand_name": "MemoryMaker", 
                "description": "Custom photo collage frame that holds 12 favorite family memories",
                "features": "Holds 12 photos, Personalized engraving, Solid wood construction, Multiple layouts",
                "price": 34.99,
                "categories": "Home Decor, Photo Frames",
                "brand_tone": "casual",
                "occasion": "Mother's Day",
                "target_keywords": "photo frame, personalized gift, family memories"
            }
        },
        {
            "name": "Regular Listing + Professional Tone",
            "data": {
                "name": "Ergonomic Office Chair",
                "brand_name": "WorkComfort", 
                "description": "Professional ergonomic office chair designed for all-day comfort",
                "features": "Lumbar support, Adjustable height, Breathable mesh, 5-year warranty",
                "price": 299.99,
                "categories": "Office Furniture, Chairs",
                "brand_tone": "professional",
                "occasion": "",  # No occasion
                "target_keywords": "office chair, ergonomic, lumbar support"
            }
        }
    ]
    
    print("COMPREHENSIVE OCCASION TESTING")
    print("=" * 60)
    
    results = []
    
    for i, scenario in enumerate(test_scenarios):
        print(f"\nTEST {i+1}: {scenario['name']}")
        print(f"Occasion: '{scenario['data']['occasion']}'")
        print(f"Tone: {scenario['data']['brand_tone']}")
        
        try:
            # Create product
            product_data = scenario['data'].copy()
            product_data["target_platform"] = "amazon"
            
            create_response = requests.post(
                f"{base_url}/core/products/",
                json=product_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if create_response.status_code in [200, 201]:
                product_result = create_response.json()
                product_id = product_result.get('id')
                print(f"Product created: ID {product_id}")
                
                # Generate listing
                print("Generating Amazon listing...")
                
                listing_response = requests.post(
                    f"{base_url}/listings/generate/{product_id}/amazon/",
                    headers={"Content-Type": "application/json"},
                    timeout=120  # Longer timeout for AI generation
                )
                
                if listing_response.status_code in [200, 201]:
                    listing_data = listing_response.json()
                    listing_id = listing_data.get('id')
                    
                    # Analyze the generated content
                    analysis = analyze_listing_content(listing_data, scenario['data'])
                    
                    results.append({
                        'scenario': scenario['name'],
                        'product_id': product_id,
                        'listing_id': listing_id,
                        'analysis': analysis,
                        'status': 'SUCCESS'
                    })
                    
                    print(f"Listing generated: ID {listing_id}")
                    print_analysis_summary(analysis)
                    
                else:
                    print(f"Listing generation failed: {listing_response.status_code}")
                    if hasattr(listing_response, 'text'):
                        print(f"Error: {listing_response.text[:200]}")
                    results.append({
                        'scenario': scenario['name'],
                        'product_id': product_id,
                        'status': 'LISTING_FAILED'
                    })
            else:
                print(f"Product creation failed: {create_response.status_code}")
                results.append({
                    'scenario': scenario['name'],
                    'status': 'PRODUCT_FAILED'
                })
                
        except Exception as e:
            print(f"Test failed with error: {str(e)}")
            results.append({
                'scenario': scenario['name'],
                'status': 'ERROR',
                'error': str(e)
            })
    
    # Final summary
    print("\n" + "=" * 60)
    print("COMPREHENSIVE TEST RESULTS")
    print("=" * 60)
    
    successful_tests = [r for r in results if r.get('status') == 'SUCCESS']
    print(f"Successful tests: {len(successful_tests)}/{len(results)}")
    
    if successful_tests:
        print("\nDetailed Analysis:")
        for result in successful_tests:
            print(f"\n{result['scenario']}:")
            analysis = result['analysis']
            print(f"  - Occasion emphasis: {analysis['occasion_emphasis']}/10")
            print(f"  - A+ content adaptation: {analysis['aplus_adaptation']}/10")
            print(f"  - Keyword strategy: {analysis['keyword_strategy']}/10")
            print(f"  - Title optimization: {analysis['title_optimization']}/10")
            print(f"  - Overall score: {analysis['overall_score']}/10")
    
    return results

def analyze_listing_content(listing_data, original_data):
    """Analyze how well the listing incorporates occasion data"""
    
    occasion = original_data.get('occasion', '').lower()
    tone = original_data.get('brand_tone', '').lower()
    
    analysis = {
        'occasion_emphasis': 0,
        'aplus_adaptation': 0,  
        'keyword_strategy': 0,
        'title_optimization': 0,
        'tone_adaptation': 0,
        'details': {}
    }
    
    # Extract content fields
    title = listing_data.get('title', '').lower()
    description = listing_data.get('product_description', '').lower()
    bullets = str(listing_data.get('bullet_points', [])).lower()
    keywords = listing_data.get('seo_keywords', {})
    aplus_content = listing_data.get('a_plus_content', {})
    
    # Analyze occasion emphasis (if occasion exists)
    if occasion:
        occasion_keywords = get_occasion_keywords(occasion)
        
        # Check title for occasion keywords
        title_score = 0
        for keyword in occasion_keywords:
            if keyword in title:
                title_score += 2
        analysis['occasion_emphasis'] = min(title_score, 10)
        analysis['details']['occasion_in_title'] = title_score > 0
        
        # Check description for occasion emphasis
        desc_score = 0
        for keyword in occasion_keywords:
            if keyword in description:
                desc_score += 1
        analysis['details']['occasion_in_description'] = desc_score > 0
        
        # Check bullets for occasion references
        bullet_score = 0
        for keyword in occasion_keywords:
            if keyword in bullets:
                bullet_score += 1
        analysis['details']['occasion_in_bullets'] = bullet_score > 0
        
    else:
        # No occasion - should be general purpose
        analysis['occasion_emphasis'] = 10  # Perfect for no occasion
        analysis['details']['no_occasion_appropriate'] = True
    
    # Analyze A+ content adaptation
    aplus_score = 0
    if isinstance(aplus_content, dict):
        # Check if A+ content sections exist
        sections_count = len([k for k in aplus_content.keys() if k.startswith('section')])
        aplus_score += min(sections_count * 2, 6)
        
        # Check for occasion-specific adaptation in A+ content
        if occasion:
            aplus_text = str(aplus_content).lower()
            occasion_keywords = get_occasion_keywords(occasion)
            for keyword in occasion_keywords:
                if keyword in aplus_text:
                    aplus_score += 1
                    
    analysis['aplus_adaptation'] = min(aplus_score, 10)
    
    # Analyze keyword strategy
    keyword_score = 0
    if isinstance(keywords, dict):
        primary_kw = keywords.get('primary', [])
        longtail_kw = keywords.get('longTail', [])
        
        # Check for keyword variety
        total_keywords = len(primary_kw) + len(longtail_kw)
        keyword_score += min(total_keywords // 10, 5)
        
        # Check for occasion-specific keywords
        if occasion:
            occasion_keywords = get_occasion_keywords(occasion)
            all_keywords = str(keywords).lower()
            for occ_kw in occasion_keywords:
                if occ_kw in all_keywords:
                    keyword_score += 1
                    
    analysis['keyword_strategy'] = min(keyword_score, 10)
    
    # Analyze title optimization
    title_score = 0
    if len(title) > 0:
        # Check length (should be under 200 characters)
        if 50 <= len(title) <= 200:
            title_score += 3
        # Check for brand name
        if original_data.get('brand_name', '').lower() in title:
            title_score += 2
        # Check for primary keywords
        if original_data.get('target_keywords'):
            target_kw = original_data['target_keywords'].split(',')[0].strip().lower()
            if target_kw in title:
                title_score += 3
        # Check for occasion (if applicable)
        if occasion:
            occasion_keywords = get_occasion_keywords(occasion)
            for keyword in occasion_keywords[:2]:  # Check first 2 occasion keywords
                if keyword in title:
                    title_score += 2
                    break
                    
    analysis['title_optimization'] = min(title_score, 10)
    
    # Calculate overall score
    scores = [analysis[key] for key in ['occasion_emphasis', 'aplus_adaptation', 'keyword_strategy', 'title_optimization']]
    analysis['overall_score'] = sum(scores) // len(scores)
    
    return analysis

def get_occasion_keywords(occasion):
    """Get relevant keywords for an occasion"""
    keyword_map = {
        'christmas': ['christmas', 'holiday', 'gift', 'festive', 'xmas', 'seasonal', 'winter'],
        'valentine': ['valentine', 'love', 'romantic', 'romance', 'heart', 'couple', 'date'],
        'valentines': ['valentine', 'love', 'romantic', 'romance', 'heart', 'couple', 'date'],
        'mother': ['mother', 'mom', 'maternal', 'caring', 'appreciation', 'family'],
        'mothers': ['mother', 'mom', 'maternal', 'caring', 'appreciation', 'family'],
        'father': ['father', 'dad', 'paternal', 'masculine', 'appreciation', 'family'],
        'fathers': ['father', 'dad', 'paternal', 'masculine', 'appreciation', 'family'],
        'birthday': ['birthday', 'celebration', 'party', 'special', 'milestone', 'age'],
        'wedding': ['wedding', 'marriage', 'bride', 'groom', 'ceremony', 'celebration'],
        'graduation': ['graduation', 'achievement', 'success', 'milestone', 'education', 'degree']
    }
    
    # Try to find exact match or partial match
    for key, keywords in keyword_map.items():
        if key in occasion.lower() or occasion.lower() in key:
            return keywords
            
    # If no match, return the occasion itself
    return [occasion.lower()]

def print_analysis_summary(analysis):
    """Print a quick summary of the analysis"""
    print(f"  - Occasion emphasis: {analysis['occasion_emphasis']}/10")
    print(f"  - A+ adaptation: {analysis['aplus_adaptation']}/10")
    print(f"  - Keyword strategy: {analysis['keyword_strategy']}/10") 
    print(f"  - Title optimization: {analysis['title_optimization']}/10")
    print(f"  - Overall: {analysis['overall_score']}/10")

if __name__ == "__main__":
    try:
        results = test_comprehensive_occasions()
        
        # Check if we have any successful results
        successful = [r for r in results if r.get('status') == 'SUCCESS']
        if successful:
            print(f"\nTesting completed with {len(successful)} successful tests")
            sys.exit(0)
        else:
            print(f"\nTesting completed but no successful generations")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        sys.exit(1)