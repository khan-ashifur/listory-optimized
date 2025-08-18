#!/usr/bin/env python3
"""
TEST TURKEY A+ CONTENT GENERATION SPECIFICALLY
Force proper Turkish A+ content generation and check the AI response
"""

import os
import sys
import django
import json
from datetime import datetime

# Add backend to Python path
backend_path = os.path.join(os.getcwd(), 'backend')
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.services import ListingGeneratorService
from apps.core.models import Product

def test_turkey_aplus_specific():
    """Test Turkey A+ content generation with focused analysis"""
    
    print("🇹🇷 TURKEY A+ CONTENT GENERATION TEST")
    print("=" * 50)
    
    # Create test product for Turkey
    from django.contrib.auth.models import User
    user, created = User.objects.get_or_create(username='test_aplus_turkey')
    
    product = Product.objects.create(
        user=user,
        name="Premium Bluetooth Kulaklık Seti",
        brand_name="TechPro",
        marketplace="tr",
        marketplace_language="tr", 
        price=299.99,
        occasion="yeni_yil",
        brand_tone="luxury",
        categories="Electronics > Audio",
        description="Yüksek kaliteli Bluetooth kulaklık seti premium ses deneyimi için. Türk aileleri için tasarlanmış rahat kullanım.",
        features="Bluetooth 5.3 teknolojisi\n30 saat pil ömrü\nGürültü engelleme\nIPX5 su direnci\nHızlı şarj"
    )
    
    print(f"✅ Product Created: {product.name}")
    print(f"📍 Marketplace: {product.marketplace}")
    print()
    
    # Generate listing
    service = ListingGeneratorService()
    
    try:
        print("🤖 Generating Turkey listing...")
        listing = service.generate_listing(product.id, 'amazon')
        
        print(f"📊 Status: {listing.status}")
        print()
        
        # Analyze A+ content
        print("🎨 A+ CONTENT DETAILED ANALYSIS:")
        print("=" * 40)
        
        if listing.amazon_aplus_content:
            aplus_content = listing.amazon_aplus_content
            
            print(f"✅ A+ Content Generated: {len(aplus_content):,} characters")
            
            # Check for Turkish language content
            turkish_words = ['türk', 'kalite', 'garanti', 'ürün', 'müşteri', 'aile', 'teknoloji', 'kullanım']
            turkish_found = 0
            for word in turkish_words:
                if word in aplus_content.lower():
                    turkish_found += 1
            
            print(f"🇹🇷 Turkish Content Indicators: {turkish_found}/{len(turkish_words)} found")
            
            # Look for specific sections
            sections_found = []
            if 'Hero Section' in aplus_content or 'Hero' in aplus_content:
                sections_found.append('Hero')
            if 'Features' in aplus_content or 'Özellik' in aplus_content:
                sections_found.append('Features')
            if 'FAQ' in aplus_content or 'Soru' in aplus_content:
                sections_found.append('FAQ')
            if 'Trust' in aplus_content or 'Güven' in aplus_content:
                sections_found.append('Trust')
            
            print(f"📋 Sections Found: {', '.join(sections_found)}")
            
            # Extract meaningful Turkish content
            lines = aplus_content.split('\n')
            turkish_content_lines = []
            
            for line in lines:
                # Look for lines with substantial Turkish content
                if any(word in line.lower() for word in turkish_words) and len(line.strip()) > 20:
                    # Remove HTML tags for cleaner display
                    clean_line = line.strip()
                    if not clean_line.startswith('<') and not clean_line.endswith('>'):
                        turkish_content_lines.append(clean_line)
            
            print(f"🗣️ Turkish Content Lines Found: {len(turkish_content_lines)}")
            if turkish_content_lines:
                print("📄 Sample Turkish Content:")
                for i, line in enumerate(turkish_content_lines[:5], 1):
                    print(f"   {i}. {line[:100]}...")
            
            # Check for proper A+ structure
            if '<div class="aplus-section">' in aplus_content:
                section_count = aplus_content.count('<div class="aplus-section">')
                print(f"✅ Proper A+ Sections: {section_count} found")
            else:
                print("❌ No proper A+ sections found (generic template used)")
            
            # Save the full A+ content for inspection
            with open(f'turkey_aplus_full_content_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html', 'w', encoding='utf-8') as f:
                f.write(aplus_content)
            
            print(f"💾 Full A+ content saved to turkey_aplus_full_content_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
            
        else:
            print("❌ NO A+ CONTENT GENERATED!")
        
        # Also check the individual fields that should feed into A+ content
        print("\n🔍 A+ COMPONENT FIELDS:")
        print("=" * 30)
        
        hero_title = getattr(listing, 'hero_title', '')
        hero_content = getattr(listing, 'hero_content', '')
        features = getattr(listing, 'features', '')
        trust_builders = getattr(listing, 'trust_builders', '')
        faqs = getattr(listing, 'faqs', '')
        
        print(f"Hero Title: {len(hero_title)} chars")
        if hero_title:
            print(f"   Preview: {hero_title[:100]}...")
        
        print(f"Hero Content: {len(hero_content)} chars")
        if hero_content:
            print(f"   Preview: {hero_content[:100]}...")
            
        print(f"Features: {len(features)} chars")
        if features:
            feature_lines = features.split('\n')[:3]
            for i, feature in enumerate(feature_lines, 1):
                if feature.strip():
                    print(f"   Feature {i}: {feature.strip()[:80]}...")
        
        print(f"Trust Builders: {len(trust_builders)} chars")
        if trust_builders:
            trust_lines = trust_builders.split('\n')[:2]
            for i, trust in enumerate(trust_lines, 1):
                if trust.strip():
                    print(f"   Trust {i}: {trust.strip()[:80]}...")
        
        print(f"FAQs: {len(faqs)} chars")
        if faqs:
            print(f"   Preview: {faqs[:100]}...")
        
        # Summary assessment
        print(f"\n🎯 A+ CONTENT ASSESSMENT:")
        print("=" * 30)
        
        if listing.amazon_aplus_content and len(listing.amazon_aplus_content) > 5000:
            print("✅ A+ Content Generated Successfully")
            if turkish_found >= 5:
                print("✅ Turkish Localization Detected")
            else:
                print("⚠️ Limited Turkish Localization")
            
            if sections_found:
                print(f"✅ Structured Sections: {len(sections_found)}")
            else:
                print("⚠️ Generic Template Used")
        else:
            print("❌ A+ Content Generation Failed")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        product.delete()
        print(f"\n🧹 Test product cleaned up")

if __name__ == "__main__":
    test_turkey_aplus_specific()