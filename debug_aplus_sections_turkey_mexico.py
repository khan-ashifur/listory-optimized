#!/usr/bin/env python3

"""
Debug A+ Content Sections for Turkey vs Mexico
Check exact A+ content structure and sections generated
"""

import os
import sys
import django
import json

# Django setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from django.contrib.auth.models import User

def debug_aplus_sections():
    """Debug A+ content sections for Turkey vs Mexico"""
    print("🔍 A+ CONTENT SECTIONS DEBUG - TURKEY vs MEXICO")
    print("=" * 70)
    
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username='aplus_debug')
    
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
    
    for market in markets:
        print(f"\n{market['flag']} ANALYZING {market['name'].upper()} A+ CONTENT STRUCTURE")
        print("-" * 60)
        
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
                
                print(f"✅ Total A+ Content Length: {len(aplus_content)} characters")
                
                # Look for section titles in A+ content
                import re
                
                # Find sections with different patterns
                patterns = [
                    r'<h2[^>]*>([^<]+)</h2>',  # Standard h2 sections
                    r'<h3[^>]*>([^<]+)</h3>',  # Standard h3 sections  
                    r'class="text-xl[^"]*"[^>]*>([^<]+)<',  # Tailwind sections
                    r'section-title[^>]*>([^<]+)<',  # Custom section titles
                    r'<strong[^>]*>([^<]*(?:Section|Strategy|Content)[^<]*)</strong>'  # Strategy sections
                ]
                
                all_sections = []
                for pattern in patterns:
                    sections = re.findall(pattern, aplus_content, re.IGNORECASE)
                    all_sections.extend(sections)
                
                # Clean and deduplicate sections
                unique_sections = []
                seen = set()
                for section in all_sections:
                    clean_section = re.sub(r'[^\w\s]', '', section.strip())
                    if clean_section and clean_section.lower() not in seen and len(clean_section) > 3:
                        unique_sections.append(section.strip())
                        seen.add(clean_section.lower())
                
                print(f"📋 DETECTED A+ SECTIONS ({len(unique_sections)} found):")
                for i, section in enumerate(unique_sections[:10], 1):  # Show first 10
                    print(f"   {i}. {section}")
                
                if len(unique_sections) > 10:
                    print(f"   ... and {len(unique_sections) - 10} more sections")
                
                # Check for specific content patterns Mexico should have
                mexico_patterns = [
                    "Audífonos Traductores Sensei",
                    "Garantizado para Familias", 
                    "Customer Satisfaction",
                    "Usage",
                    "Quality",
                    "Features"
                ]
                
                turkey_patterns = [
                    "Sensei AI Çeviri Kulaklık",
                    "Türk Ailesi için",
                    "Müşteri Memnuniyeti", 
                    "Kullanım",
                    "Kalite",
                    "Özellikler"
                ]
                
                # Check content depth
                if market['code'] == 'mx':
                    print(f"\n🇲🇽 MEXICO CONTENT ANALYSIS:")
                    for pattern in mexico_patterns:
                        if pattern.lower() in aplus_content.lower():
                            print(f"   ✅ Found: {pattern}")
                        else:
                            print(f"   ❌ Missing: {pattern}")
                            
                elif market['code'] == 'tr':
                    print(f"\n🇹🇷 TURKEY CONTENT ANALYSIS:")
                    for pattern in turkey_patterns:
                        if pattern.lower() in aplus_content.lower():
                            print(f"   ✅ Found: {pattern}")
                        else:
                            print(f"   ❌ Missing: {pattern}")
                
                # Check for detailed sections vs basic structure
                basic_indicators = ["Complete A+ Content Strategy", "Overall A+ Strategy"]
                detailed_indicators = ["Hero", "Features", "Quality", "Usage", "Customer Satisfaction", "Comparison", "FAQ", "What's in Box"]
                
                basic_count = sum(1 for indicator in basic_indicators if indicator.lower() in aplus_content.lower())
                detailed_count = sum(1 for indicator in detailed_indicators if indicator.lower() in aplus_content.lower())
                
                print(f"\n📊 CONTENT DEPTH ANALYSIS:")
                print(f"   Basic structure indicators: {basic_count}/2")
                print(f"   Detailed section indicators: {detailed_count}/8")
                
                if detailed_count >= 6:
                    print(f"   ✅ COMPREHENSIVE: Has detailed sections")
                elif basic_count >= 1:
                    print(f"   ⚠️ BASIC: Only basic structure")
                else:
                    print(f"   ❌ MINIMAL: Very limited content")
                
                # Show a sample of the content structure
                print(f"\n📝 CONTENT SAMPLE (first 500 chars):")
                print(f"   {aplus_content[:500]}...")
                
            else:
                print(f"❌ No A+ content generated")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        # Cleanup
        product.delete()
        print()

if __name__ == "__main__":
    debug_aplus_sections()