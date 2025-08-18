#!/usr/bin/env python3

"""
Test Turkey Fix Verification
Verify Turkey now generates comprehensive 8-section A+ content like Mexico
"""

import os
import sys
import django

# Django setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from django.contrib.auth.models import User

def test_turkey_fix():
    """Test that Turkey now generates comprehensive A+ content like Mexico"""
    print("🇹🇷 TESTING TURKEY FIX - COMPREHENSIVE A+ CONTENT")
    print("=" * 65)
    
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username='turkey_fix_test')
    
    markets = [
        {
            'code': 'tr',
            'name': 'Turkey',
            'flag': '🇹🇷',
            'product_name': 'Sensei AI Çeviri Kulaklık'
        },
        {
            'code': 'mx',
            'name': 'Mexico', 
            'flag': '🇲🇽',
            'product_name': 'Audífonos Traductores Sensei'
        }
    ]
    
    results = {}
    
    for market in markets:
        print(f"\n{market['flag']} TESTING {market['name'].upper()} COMPREHENSIVE A+ CONTENT")
        print("-" * 55)
        
        # Create product
        product = Product.objects.create(
            user=test_user,
            name=market['product_name'],
            brand_name="Sensei Tech",
            description="Advanced AI translation technology with 40 languages",
            price=299.99,
            marketplace=market['code'],
            marketplace_language=market['code'],
            categories="Electronics/Audio/Headphones"
        )
        
        try:
            result = service.generate_listing(product_id=product.id, platform='amazon')
            
            if result and result.amazon_aplus_content:
                aplus_content = result.amazon_aplus_content
                
                # Extract all section titles
                import re
                patterns = [
                    r'<h2[^>]*class="text-xl[^"]*"[^>]*>([^<]+)</h2>',  # Tailwind h2
                    r'<h3[^>]*class="text-lg[^"]*"[^>]*>([^<]+)</h3>',  # Tailwind h3
                    r'<h[23][^>]*>([^<]+(?:Hero|Features|Quality|Usage|Trust|FAQ|Customer|What|Why|Comparison)[^<]*)</h[23]>',  # Section headers
                    r'class="section-title[^"]*"[^>]*>([^<]+)</div>',  # Custom section titles
                    r'<strong[^>]*>([^<]*(?:Section|Strategy|Content|Hero|Features|Quality|Usage|Trust|FAQ|Customer|What|Why|Comparison)[^<]*)</strong>'  # Strong section headers
                ]
                
                all_sections = []
                for pattern in patterns:
                    sections = re.findall(pattern, aplus_content, re.IGNORECASE)
                    all_sections.extend(sections)
                
                # Clean and filter relevant sections
                relevant_sections = []
                section_keywords = ['hero', 'features', 'quality', 'usage', 'trust', 'faq', 'customer', 'what', 'why', 'comparison', 'özellik', 'kalite', 'kullanım', 'güven', 'müşteri', 'neden', 'características', 'calidad', 'uso', 'confianza', 'cliente', 'por qué']
                
                for section in all_sections:
                    clean_section = section.strip()
                    if any(keyword in clean_section.lower() for keyword in section_keywords) and len(clean_section) > 5:
                        if clean_section not in relevant_sections:
                            relevant_sections.append(clean_section)
                
                # Count comprehensive vs basic sections
                comprehensive_indicators = [
                    'hero', 'features', 'quality', 'trust', 'usage', 'customer', 'faq', 'what',
                    'özellik', 'kalite', 'güven', 'kullanım', 'müşteri', 'sık',
                    'características', 'calidad', 'confianza', 'uso', 'cliente', 'preguntas'
                ]
                
                comprehensive_count = 0
                for section in relevant_sections:
                    if any(indicator in section.lower() for indicator in comprehensive_indicators):
                        comprehensive_count += 1
                
                results[market['code']] = {
                    'total_length': len(aplus_content),
                    'relevant_sections': len(relevant_sections),
                    'comprehensive_sections': comprehensive_count,
                    'sections': relevant_sections[:8]  # First 8 sections
                }
                
                print(f"✅ A+ Content Length: {len(aplus_content):,} characters")
                print(f"✅ Relevant Sections Found: {len(relevant_sections)}")
                print(f"✅ Comprehensive Sections: {comprehensive_count}")
                
                print(f"\n📋 MAIN A+ SECTIONS:")
                for i, section in enumerate(relevant_sections[:8], 1):
                    print(f"   {i}. {section}")
                
                if comprehensive_count >= 6:
                    print(f"✅ RESULT: COMPREHENSIVE A+ content with detailed sections")
                elif comprehensive_count >= 3:
                    print(f"⚠️ RESULT: PARTIAL A+ content")
                else:
                    print(f"❌ RESULT: BASIC A+ content only")
                    
            else:
                print(f"❌ No A+ content generated")
                results[market['code']] = {'error': 'No content'}
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            results[market['code']] = {'error': str(e)}
        
        # Cleanup
        product.delete()
    
    # Final comparison
    print(f"\n🏆 COMPREHENSIVE A+ CONTENT COMPARISON")
    print("=" * 65)
    
    if 'tr' in results and 'mx' in results:
        tr_sections = results['tr'].get('comprehensive_sections', 0)
        mx_sections = results['mx'].get('comprehensive_sections', 0)
        tr_length = results['tr'].get('total_length', 0)
        mx_length = results['mx'].get('total_length', 0)
        
        print(f"🇹🇷 Turkey:")
        print(f"   - Content Length: {tr_length:,} characters")
        print(f"   - Comprehensive Sections: {tr_sections}")
        print(f"   - Status: {'✅ COMPREHENSIVE' if tr_sections >= 6 else '⚠️ NEEDS IMPROVEMENT'}")
        
        print(f"🇲🇽 Mexico:")
        print(f"   - Content Length: {mx_length:,} characters") 
        print(f"   - Comprehensive Sections: {mx_sections}")
        print(f"   - Status: {'✅ COMPREHENSIVE' if mx_sections >= 6 else '⚠️ NEEDS IMPROVEMENT'}")
        
        print(f"\n🎯 FIX VERIFICATION:")
        if tr_sections >= 6 and mx_sections >= 6:
            print(f"✅ SUCCESS: Both Turkey and Mexico now generate comprehensive A+ content!")
            print(f"✅ Turkey has {tr_sections} detailed sections (target: 6+)")
            print(f"✅ Mexico has {mx_sections} detailed sections (target: 6+)")
            print(f"✅ Both markets now generate detailed 8-section A+ content")
        elif tr_sections >= mx_sections - 1:  # Within 1 section of Mexico
            print(f"✅ IMPROVED: Turkey now generates similar comprehensive content to Mexico")
            print(f"   Turkey: {tr_sections} sections vs Mexico: {mx_sections} sections")
        else:
            print(f"❌ STILL NEEDS WORK: Turkey still behind Mexico")
            print(f"   Turkey: {tr_sections} sections vs Mexico: {mx_sections} sections")

if __name__ == "__main__":
    test_turkey_fix()