#!/usr/bin/env python3
"""
Comprehensive Sweden Market Implementation Test
Tests multiple product types and scenarios to ensure robust Swedish implementation
"""

import os
import sys
import django
import json
from datetime import datetime

# Add the backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(backend_path)

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from apps.listings.models import GeneratedListing
from django.contrib.auth.models import User

def create_test_products():
    """Create multiple test products for comprehensive testing"""
    
    # Get or create test user
    user, created = User.objects.get_or_create(
        username='testuser_se',
        defaults={'email': 'test_se@example.com'}
    )
    
    # Clean up old test products
    Product.objects.filter(name__icontains="Swedish Test").delete()
    
    test_products = [
        {
            'name': 'Swedish Test Kitchen Coffee Maker',
            'description': 'Premium automatic coffee maker perfect for Swedish homes. Features sustainable brewing technology and minimalist Scandinavian design.',
            'brand_name': 'NordicBrew',
            'categories': 'Kitchen, Coffee, Appliances',
            'target_keywords': 'kaffebryggare, automatisk kaffe, hållbar brewing, svensk design, kök',
            'occasion': 'fika',  # Swedish coffee culture
            'features': 'Automatic brewing, Eco-friendly, Minimalist design, Timer function, Swedish quality standards'
        },
        {
            'name': 'Swedish Test Outdoor Camping Gear',
            'description': 'Durable camping equipment designed for Swedish nature adventures. Perfect for allemansrätten outdoor activities.',
            'brand_name': 'SwedenOutdoor',
            'categories': 'Sports, Outdoor, Camping',
            'target_keywords': 'camping utrustning, utomhusaktiviteter, allemansrätten, vandring, friluftsliv',
            'occasion': 'sommarstuga',  # Summer cottage
            'features': 'Weather resistant, Lightweight, Sustainable materials, Swedish design, Nature-friendly'
        },
        {
            'name': 'Swedish Test Christmas Decorations',
            'description': 'Traditional Swedish Christmas decorations combining lucia traditions with modern design. Perfect for creating hygge atmosphere.',
            'brand_name': 'LuciaLights',
            'categories': 'Home, Decorations, Christmas',
            'target_keywords': 'juldekorationer, lucia ljus, svensk tradition, hygge, hem inredning',
            'occasion': 'lucia',  # Saint Lucia Day
            'features': 'Traditional Swedish design, LED lights, Sustainable materials, Handcrafted quality, Festive atmosphere'
        }
    ]
    
    created_products = []
    for product_data in test_products:
        product_data.update({
            'user': user,
            'brand_tone': 'professional',
            'target_platform': 'amazon',
            'marketplace': 'se',
            'marketplace_language': 'sv',
            'price': 599.00,
            'target_audience': 'Swedish families, professionals, nature lovers'
        })
        
        product = Product.objects.create(**product_data)
        created_products.append(product)
        print(f"✅ Created: {product.name} (ID: {product.id}) - Occasion: {product.occasion}")
    
    return created_products

def analyze_swedish_implementation(listing):
    """Comprehensive analysis of Swedish implementation quality"""
    
    analysis = {
        'title_analysis': {},
        'bullet_analysis': {},
        'description_analysis': {},
        'keywords_analysis': {},
        'occasions_analysis': {},
        'cultural_adaptation': {},
        'overall_score': 0
    }
    
    # Title Analysis
    title = listing.title
    analysis['title_analysis'] = {
        'length': len(title),
        'has_swedish_words': bool(['hörlurar', 'kaffebryggare', 'camping', 'juldekorationer'] and any(word in title.lower() for word in ['hörlurar', 'kaffebryggare', 'camping', 'juldekorationer'])),
        'has_quality_indicators': bool(['Bäst i Test', 'Premium', 'Kvalitet', 'CE-märkt'] and any(indicator in title for indicator in ['Bäst i Test', 'Premium', 'Kvalitet', 'CE-märkt'])),
        'has_swedish_special_chars': bool('ä' in title or 'ö' in title or 'å' in title),
        'has_occasion_reference': bool(['Jul', 'Lucia', 'Midsommar', 'Fika'] and any(occ in title for occ in ['Jul', 'Lucia', 'Midsommar', 'Fika'])),
        'has_guarantee_info': bool('garanti' in title.lower() or 'års' in title.lower())
    }
    
    # Bullet Analysis
    bullet_text = str(listing.bullet_points)
    analysis['bullet_analysis'] = {
        'has_swedish_formatting': bool(['CERTIFIED', 'PROVEN', 'OPTIMIZED', 'VALIDATED'] and any(format_word in bullet_text for format_word in ['CERTIFIED', 'PROVEN', 'OPTIMIZED', 'VALIDATED'])),
        'has_swedish_content': bool(['svenska', 'svensk', 'Sverige', 'nordisk'] and any(content in bullet_text.lower() for content in ['svenska', 'svensk', 'sverige', 'nordisk'])),
        'has_sustainability_focus': bool(['miljövänlig', 'hållbar', 'ekologisk', 'återvinning'] and any(sust in bullet_text.lower() for sust in ['miljövänlig', 'hållbar', 'ekologisk', 'återvinning'])),
        'has_cultural_references': bool(['fika', 'lagom', 'hygge', 'allemansrätt'] and any(culture in bullet_text.lower() for culture in ['fika', 'lagom', 'hygge', 'allemansrätt'])),
        'has_practical_benefits': bool(['praktisk', 'bekväm', 'enkel', 'effektiv'] and any(practical in bullet_text.lower() for practical in ['praktisk', 'bekväm', 'enkel', 'effektiv']))
    }
    
    # Description Analysis
    desc_text = listing.long_description.lower()
    analysis['description_analysis'] = {
        'length': len(listing.long_description),
        'has_quality_focus': bool(['kvalitet', 'standard', 'certifierad', 'testad'] and any(quality in desc_text for quality in ['kvalitet', 'standard', 'certifierad', 'testad'])),
        'has_swedish_values': bool(['hållbarhet', 'miljötänk', 'kvalitet', 'trygghet'] and any(value in desc_text for value in ['hållbarhet', 'miljötänk', 'kvalitet', 'trygghet'])),
        'has_local_context': bool(['svensk', 'nordisk', 'skandinavisk'] and any(local in desc_text for local in ['svensk', 'nordisk', 'skandinavisk'])),
        'mentions_guarantee': bool('garanti' in desc_text or 'trygghet' in desc_text)
    }
    
    # Keywords Analysis
    all_keywords = str(listing.amazon_keywords) + " " + str(listing.amazon_backend_keywords)
    analysis['keywords_analysis'] = {
        'has_swedish_keywords': bool(['hörlurar', 'kaffebryggare', 'utomhus', 'jul'] and any(kw in all_keywords.lower() for kw in ['hörlurar', 'kaffebryggare', 'utomhus', 'jul'])),
        'has_cultural_keywords': bool(['fika', 'hygge', 'lagom', 'allemansrätt'] and any(culture in all_keywords.lower() for culture in ['fika', 'hygge', 'lagom', 'allemansrätt'])),
        'has_quality_keywords': bool(['kvalitet', 'premium', 'certifierad', 'garanti'] and any(quality in all_keywords.lower() for quality in ['kvalitet', 'premium', 'certifierad', 'garanti'])),
        'has_sustainability_keywords': bool(['hållbar', 'miljövänlig', 'ekologisk'] and any(sust in all_keywords.lower() for sust in ['hållbar', 'miljövänlig', 'ekologisk']))
    }
    
    # Occasions Analysis
    content_text = title + " " + listing.long_description + " " + bullet_text
    swedish_occasions = ['jul', 'lucia', 'midsommar', 'valborg', 'fika', 'sommarstuga', 'hygge']
    found_occasions = [occ for occ in swedish_occasions if occ.lower() in content_text.lower()]
    
    analysis['occasions_analysis'] = {
        'found_occasions': found_occasions,
        'occasion_count': len(found_occasions),
        'has_seasonal_relevance': len(found_occasions) > 0,
        'culturally_appropriate': len(found_occasions) > 0
    }
    
    # Cultural Adaptation Score
    cultural_elements = [
        analysis['title_analysis']['has_swedish_special_chars'],
        analysis['bullet_analysis']['has_sustainability_focus'],
        analysis['bullet_analysis']['has_cultural_references'],
        analysis['description_analysis']['has_swedish_values'],
        analysis['keywords_analysis']['has_cultural_keywords'],
        analysis['occasions_analysis']['has_seasonal_relevance']
    ]
    
    analysis['cultural_adaptation'] = {
        'elements_present': sum(cultural_elements),
        'total_elements': len(cultural_elements),
        'adaptation_score': sum(cultural_elements) / len(cultural_elements) * 100
    }
    
    # Overall Score
    all_checks = [
        analysis['title_analysis']['has_quality_indicators'],
        analysis['title_analysis']['has_swedish_special_chars'],
        analysis['bullet_analysis']['has_swedish_formatting'],
        analysis['bullet_analysis']['has_sustainability_focus'],
        analysis['description_analysis']['has_quality_focus'],
        analysis['description_analysis']['has_local_context'],
        analysis['keywords_analysis']['has_swedish_keywords'],
        analysis['occasions_analysis']['has_seasonal_relevance']
    ]
    
    analysis['overall_score'] = sum(all_checks) / len(all_checks) * 100
    
    return analysis

def test_comprehensive_swedish_implementation():
    """Test comprehensive Swedish implementation"""
    
    print("🇸🇪 COMPREHENSIVE SWEDISH MARKET TESTING")
    print("=" * 70)
    
    # Create test products
    products = create_test_products()
    service = ListingGeneratorService()
    
    results = []
    
    for i, product in enumerate(products, 1):
        print(f"\n🧪 TEST {i}/3: {product.name}")
        print(f"   Category: {product.categories}")
        print(f"   Occasion: {product.occasion}")
        print("-" * 50)
        
        try:
            # Generate listing
            listing = service.generate_listing(product.id, 'amazon')
            
            print(f"✅ Listing generated successfully (ID: {listing.id})")
            
            # Analyze implementation
            analysis = analyze_swedish_implementation(listing)
            
            # Display key results
            print(f"\n📊 SWEDISH IMPLEMENTATION ANALYSIS:")
            print(f"   Title: {listing.title[:80]}...")
            print(f"   Special chars (å,ä,ö): {analysis['title_analysis']['has_swedish_special_chars']}")
            print(f"   Quality indicators: {analysis['title_analysis']['has_quality_indicators']}")
            print(f"   Cultural adaptation: {analysis['cultural_adaptation']['adaptation_score']:.1f}%")
            print(f"   Found occasions: {', '.join(analysis['occasions_analysis']['found_occasions']) if analysis['occasions_analysis']['found_occasions'] else 'None'}")
            print(f"   Overall score: {analysis['overall_score']:.1f}%")
            
            results.append({
                'product': product,
                'listing': listing,
                'analysis': analysis
            })
            
        except Exception as e:
            print(f"❌ Error generating listing: {e}")
    
    # Summary Report
    print(f"\n🇸🇪 COMPREHENSIVE TEST SUMMARY")
    print("=" * 70)
    
    if results:
        avg_score = sum(r['analysis']['overall_score'] for r in results) / len(results)
        avg_cultural = sum(r['analysis']['cultural_adaptation']['adaptation_score'] for r in results) / len(results)
        
        all_occasions = []
        for r in results:
            all_occasions.extend(r['analysis']['occasions_analysis']['found_occasions'])
        unique_occasions = list(set(all_occasions))
        
        print(f"📈 PERFORMANCE METRICS:")
        print(f"   Tests completed: {len(results)}/{len(products)}")
        print(f"   Average implementation score: {avg_score:.1f}%")
        print(f"   Average cultural adaptation: {avg_cultural:.1f}%")
        print(f"   Swedish occasions detected: {', '.join(unique_occasions) if unique_occasions else 'None'}")
        
        print(f"\n🏆 DETAILED RESULTS:")
        for i, result in enumerate(results, 1):
            analysis = result['analysis']
            product = result['product']
            
            print(f"\n   TEST {i}: {product.name}")
            print(f"     • Overall score: {analysis['overall_score']:.1f}%")
            print(f"     • Cultural adaptation: {analysis['cultural_adaptation']['adaptation_score']:.1f}%")
            print(f"     • Title length: {analysis['title_analysis']['length']} chars")
            print(f"     • Description length: {analysis['description_analysis']['length']} chars")
            print(f"     • Swedish special chars: {analysis['title_analysis']['has_swedish_special_chars']}")
            print(f"     • Sustainability focus: {analysis['bullet_analysis']['has_sustainability_focus']}")
            print(f"     • Occasions: {', '.join(analysis['occasions_analysis']['found_occasions']) if analysis['occasions_analysis']['found_occasions'] else 'None'}")
        
        # Overall Assessment
        if avg_score >= 85:
            grade = "A - EXCELLENT"
            assessment = "Sweden implementation is working exceptionally well!"
        elif avg_score >= 75:
            grade = "B - GOOD"
            assessment = "Sweden implementation is solid with minor areas for improvement."
        elif avg_score >= 65:
            grade = "C - FAIR"
            assessment = "Sweden implementation is functional but needs enhancement."
        else:
            grade = "D - NEEDS WORK"
            assessment = "Sweden implementation requires significant improvements."
        
        print(f"\n🎯 FINAL ASSESSMENT:")
        print(f"   Grade: {grade}")
        print(f"   Assessment: {assessment}")
        print(f"   Cultural adaptation: {avg_cultural:.1f}% (Target: >80%)")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if avg_cultural < 80:
            print(f"   • Increase cultural references (fika, lagom, hygge, allemansrätt)")
            print(f"   • Add more Swedish occasions integration")
        if avg_score < 80:
            print(f"   • Enhance Swedish language authenticity")
            print(f"   • Improve sustainability messaging (key Swedish value)")
        
        print(f"   • Continue leveraging strong Swedish special character usage")
        print(f"   • Maintain quality-focused messaging (aligns with Swedish values)")
        
    else:
        print("❌ No successful tests completed")
    
    return results

def main():
    """Main test function"""
    print("🧪 SWEDEN MARKET COMPREHENSIVE TESTING SUITE")
    print("Testing Swedish language implementation across multiple product categories")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    results = test_comprehensive_swedish_implementation()
    
    print(f"\n✅ COMPREHENSIVE SWEDEN MARKET TEST COMPLETED!")
    print(f"Generated {len(results)} successful listings")
    print(f"Review the detailed analysis above for implementation quality assessment.")

if __name__ == "__main__":
    main()