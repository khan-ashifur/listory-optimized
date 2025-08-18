#!/usr/bin/env python3

"""
Debug Turkey Language Issue - Check why Turkey is getting Spanish content instead of Turkish
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

def test_turkey_aplus_content():
    """Test Turkey A+ content generation to identify language mixing issue"""
    print("🇹🇷 TESTING TURKEY A+ CONTENT GENERATION")
    print("=" * 60)
    
    # Create test user
    test_user, _ = User.objects.get_or_create(username='turkey_debug_test')
    
    # Create Turkey product
    product = Product.objects.create(
        user=test_user,
        name="Sensei AI Çeviri Kulaklık",
        brand_name="Sensei Tech",
        description="""Gelişmiş yapay zeka çeviri teknolojisi ile 40 dili anlık çeviren kulaklık. 
        Türk aileleri için özel tasarım ile her konuşmayı net anlarız. Premium ses kalitesi.""",
        price=299.99,
        marketplace="tr",
        marketplace_language="tr",
        categories="Electronics/Audio/Headphones",
        occasion="general"
    )
    
    try:
        service = ListingGeneratorService()
        result = service.generate_listing(product_id=product.id, platform='amazon')
        
        if result and result.amazon_aplus_content:
            aplus_content = result.amazon_aplus_content
            
            print("\n🔍 A+ CONTENT ANALYSIS:")
            print(f"📏 Length: {len(aplus_content)} characters")
            
            # Check for Spanish content (problematic)
            spanish_indicators = [
                'Audífonos', 'México', 'Garantizado', 'Familias en México',
                'premium quality', 'trusted brand',  # English keywords
                'ENGLISH: Hero lifestyle', 'ENGLISH: Turkish family'  # English image descriptions
            ]
            
            spanish_found = []
            for indicator in spanish_indicators:
                if indicator in aplus_content:
                    spanish_found.append(indicator)
            
            # Check for Turkish content (expected)
            turkish_indicators = [
                'Çeviri Kulaklık', 'Türk Aileleri', 'Garantili',
                'kaliteli', 'güvenilir marka', 'müşteri memnuniyeti',  # Turkish keywords
                'Anahtar Kelimeler', 'Görsel Strateji', 'SEO Odak'  # Turkish labels
            ]
            
            turkish_found = []
            for indicator in turkish_indicators:
                if indicator in aplus_content:
                    turkish_found.append(indicator)
            
            print(f"\n❌ SPANISH CONTENT FOUND ({len(spanish_found)} items):")
            for item in spanish_found:
                print(f"   - '{item}'")
            
            print(f"\n✅ TURKISH CONTENT FOUND ({len(turkish_found)} items):")
            for item in turkish_found:
                print(f"   - '{item}'")
            
            # Show first 1000 characters to see the structure
            print(f"\n📄 A+ CONTENT PREVIEW (First 1000 chars):")
            print("-" * 50)
            print(aplus_content[:1000])
            print("-" * 50)
            
            # Extract keyword sections specifically
            import re
            keyword_sections = re.findall(r'Keywords</strong>.*?<p class="text-gray-600">(.*?)</p>', aplus_content, re.DOTALL)
            if keyword_sections:
                print(f"\n🔑 KEYWORD SECTIONS FOUND ({len(keyword_sections)}):")
                for i, section in enumerate(keyword_sections, 1):
                    print(f"  {i}. {section.strip()}")
            
            # Extract image strategy sections
            image_sections = re.findall(r'Image Strategy</strong>.*?<p class="text-gray-600">(.*?)</p>', aplus_content, re.DOTALL)
            if image_sections:
                print(f"\n📸 IMAGE STRATEGY SECTIONS FOUND ({len(image_sections)}):")
                for i, section in enumerate(image_sections, 1):
                    print(f"  {i}. {section.strip()}")
            
            # Identify the issue
            if spanish_found and not turkish_found:
                print(f"\n🚨 CRITICAL ISSUE IDENTIFIED:")
                print(f"   Turkey is generating Spanish content instead of Turkish!")
                print(f"   Spanish items found: {len(spanish_found)}")
                print(f"   Turkish items found: {len(turkish_found)}")
            elif spanish_found and turkish_found:
                print(f"\n⚠️ MIXED LANGUAGE ISSUE:")
                print(f"   Turkey has both Spanish and Turkish content (should be Turkish only)")
            else:
                print(f"\n✅ Language seems correct")
                
        else:
            print("❌ No A+ content generated")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_turkey_aplus_content()