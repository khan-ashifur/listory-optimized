#!/usr/bin/env python3
"""
DEBUG TURKEY A+ CONTENT GENERATION
Check why A+ content is not being properly generated for Turkey market
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

def debug_turkey_aplus():
    """Debug Turkey A+ content generation"""
    
    print("🔍 DEBUGGING TURKEY A+ CONTENT GENERATION")
    print("=" * 50)
    
    # Create test product for Turkey
    from django.contrib.auth.models import User
    user, created = User.objects.get_or_create(username='test_debug_aplus')
    
    product = Product.objects.create(
        user=user,
        name="Debug Bluetooth Kulaklık",
        brand_name="DebugTech",
        marketplace="tr",
        marketplace_language="tr", 
        price=199.99,
        occasion="yeni_yil",
        brand_tone="luxury",
        categories="Electronics > Audio",
        description="Test ürün A+ content debug için",
        features="Test feature 1\nTest feature 2"
    )
    
    print(f"✅ Debug Product Created: {product.name}")
    print(f"📍 Marketplace: {product.marketplace}")
    print()
    
    # Generate listing and track A+ content specifically
    service = ListingGeneratorService()
    
    try:
        print("🤖 Generating listing and monitoring A+ content...")
        
        listing = service.generate_listing(product.id, 'amazon')
        
        print(f"📊 Generation Status: {listing.status}")
        print()
        
        # Check A+ content details
        print("🎨 A+ CONTENT ANALYSIS:")
        print("=" * 30)
        
        if listing.amazon_aplus_content:
            aplus_length = len(listing.amazon_aplus_content)
            print(f"✅ A+ Content Generated: {aplus_length:,} characters")
            
            # Count sections
            section_count = listing.amazon_aplus_content.count('<div class="aplus-section">')
            module_count = listing.amazon_aplus_content.count('<div class="aplus-module">')
            intro_count = listing.amazon_aplus_content.count('<div class="aplus-introduction">')
            
            print(f"📋 Structure Analysis:")
            print(f"   - Aplus sections: {section_count}")
            print(f"   - Aplus modules: {module_count}")
            print(f"   - Introduction sections: {intro_count}")
            
            # Check for Turkish content
            turkish_indicators = ['türk', 'aile', 'garanti', 'kalite', 'ürün']
            turkish_found = 0
            for indicator in turkish_indicators:
                if indicator in listing.amazon_aplus_content.lower():
                    turkish_found += 1
            
            print(f"🇹🇷 Turkish Content Check: {turkish_found}/{len(turkish_indicators)} indicators found")
            
            # Preview first 500 characters
            preview = listing.amazon_aplus_content[:500]
            print(f"📄 Content Preview (first 500 chars):")
            print(f"   {preview}...")
            
            # Check for HTML structure integrity
            if '<div' in listing.amazon_aplus_content and '</div>' in listing.amazon_aplus_content:
                print("✅ HTML Structure: Valid")
            else:
                print("❌ HTML Structure: Invalid")
                
        else:
            print("❌ NO A+ CONTENT GENERATED!")
            print("🔍 Checking individual fields...")
            
            print(f"Hero Title: {getattr(listing, 'hero_title', 'MISSING')}")
            print(f"Hero Content: {getattr(listing, 'hero_content', 'MISSING')}")
            print(f"Features: {getattr(listing, 'features', 'MISSING')}")
            print(f"Trust Builders: {getattr(listing, 'trust_builders', 'MISSING')}")
            print(f"FAQs: {getattr(listing, 'faqs', 'MISSING')}")
            
        print()
        
        # Check other content fields
        print("📝 OTHER CONTENT FIELDS:")
        print("=" * 25)
        print(f"Title: {len(listing.title)} chars")
        print(f"Description: {len(listing.long_description)} chars") 
        print(f"Bullet Points: {len(listing.bullet_points.split('\\n')) if listing.bullet_points else 0} bullets")
        print(f"Backend Keywords: {len(listing.amazon_backend_keywords)} chars")
        
        # Save debug info
        debug_data = {
            "timestamp": datetime.now().isoformat(),
            "product_id": product.id,
            "marketplace": "tr",
            "aplus_generated": bool(listing.amazon_aplus_content),
            "aplus_length": len(listing.amazon_aplus_content) if listing.amazon_aplus_content else 0,
            "aplus_preview": listing.amazon_aplus_content[:1000] if listing.amazon_aplus_content else None,
            "title_length": len(listing.title),
            "description_length": len(listing.long_description),
            "bullets_count": len(listing.bullet_points.split('\\n')) if listing.bullet_points else 0,
            "fields_check": {
                "hero_title": bool(getattr(listing, 'hero_title', None)),
                "hero_content": bool(getattr(listing, 'hero_content', None)),
                "features": bool(getattr(listing, 'features', None)),
                "trust_builders": bool(getattr(listing, 'trust_builders', None)),
                "faqs": bool(getattr(listing, 'faqs', None))
            }
        }
        
        with open(f'turkey_aplus_debug_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json', 'w', encoding='utf-8') as f:
            json.dump(debug_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Debug data saved to turkey_aplus_debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
    except Exception as e:
        print(f"❌ Error during generation: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        product.delete()
        print(f"🧹 Debug product cleaned up")

if __name__ == "__main__":
    debug_turkey_aplus()