#!/usr/bin/env python3
"""
Test script to check keyword generation and all sections.
"""
import os
import sys
import django
import json

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from django.contrib.auth.models import User

def test_keyword_generation():
    """Test keyword generation and check all sections."""
    print("🔍 TESTING KEYWORD GENERATION & ALL SECTIONS")
    print("=" * 60)
    
    # Get or create user
    user, _ = User.objects.get_or_create(username='testuser', defaults={'email': 'test@example.com'})
    
    # Create test product
    product = Product.objects.create(
        name='Premium Wireless Bluetooth Earbuds Pro Max',
        user=user,
        description='High-quality wireless earbuds with noise cancellation, long battery life, and premium sound quality for music lovers and professionals.',
        brand_name='AudioTech',
        brand_tone='professional',
        target_platform='amazon',
        price=129.99,
        categories='Electronics, Headphones, Wireless Earbuds, Bluetooth Audio',
        features='Active noise cancellation, 30-hour battery life, wireless charging case, premium drivers, water resistant IPX7, quick charge, touch controls',
        target_keywords='wireless earbuds, bluetooth headphones, noise cancelling earbuds, wireless audio',
        seo_keywords='best wireless earbuds 2024, bluetooth earbuds with noise cancellation, premium wireless headphones',
        long_tail_keywords='wireless earbuds with long battery life for travel, best noise cancelling earbuds for office work',
        faqs='Q: How long does the battery last? A: Up to 30 hours with charging case. Q: Are they waterproof? A: Yes, IPX7 rated for sweat and rain resistance.',
        whats_in_box='Wireless earbuds, charging case, USB-C cable, ear tips (S/M/L), user manual, warranty card',
        competitor_urls='https://www.amazon.com/competitor-earbuds'
    )
    
    print(f"✅ Created test product: {product.name}")
    
    # Generate listing
    generator = ListingGeneratorService()
    print("\n🚀 Generating Amazon listing...")
    
    try:
        listing = generator.generate_listing(product.id, 'amazon')
        
        print("\n📊 DETAILED SECTION ANALYSIS:")
        print("=" * 50)
        
        # 1. Check all basic fields
        sections_status = {}
        
        # Title
        if listing.title and len(listing.title.strip()) > 0:
            sections_status['Title'] = f"✅ {len(listing.title)} characters"
            print(f"📝 Title: ✅ {len(listing.title)} chars")
            print(f"   Content: {listing.title[:100]}...")
        else:
            sections_status['Title'] = "❌ Missing or empty"
            print(f"📝 Title: ❌ Missing or empty")
        
        # Description
        if listing.long_description and len(listing.long_description.strip()) > 0:
            sections_status['Description'] = f"✅ {len(listing.long_description)} characters"
            print(f"📄 Description: ✅ {len(listing.long_description)} chars")
            print(f"   Content: {listing.long_description[:100]}...")
        else:
            sections_status['Description'] = "❌ Missing or empty"
            print(f"📄 Description: ❌ Missing or empty")
        
        # Bullet Points
        if listing.bullet_points and len(listing.bullet_points.strip()) > 0:
            bullets = [b.strip() for b in listing.bullet_points.split('\n\n') if b.strip()]
            sections_status['Bullet Points'] = f"✅ {len(bullets)} bullets"
            print(f"🔸 Bullet Points: ✅ {len(bullets)} bullets")
            for i, bullet in enumerate(bullets[:3], 1):
                print(f"   Bullet {i}: {len(bullet)} chars - {bullet[:80]}...")
        else:
            sections_status['Bullet Points'] = "❌ Missing or empty"
            print(f"🔸 Bullet Points: ❌ Missing or empty")
        
        # 2. Check Keywords in Detail
        print(f"\n🔑 KEYWORD ANALYSIS:")
        print("-" * 30)
        
        # Short tail keywords (primary keywords)
        if listing.keywords and len(listing.keywords.strip()) > 0:
            short_tail = [k.strip() for k in listing.keywords.split(',') if k.strip()]
            sections_status['Short Tail Keywords'] = f"✅ {len(short_tail)} keywords"
            print(f"📌 Short Tail Keywords: ✅ {len(short_tail)} keywords")
            print(f"   Examples: {', '.join(short_tail[:5])}")
        else:
            sections_status['Short Tail Keywords'] = "❌ Missing or empty"
            print(f"📌 Short Tail Keywords: ❌ Missing or empty")
        
        # Long tail keywords  
        if listing.long_tail_keywords and len(listing.long_tail_keywords.strip()) > 0:
            long_tail = [k.strip() for k in listing.long_tail_keywords.split(',') if k.strip()]
            sections_status['Long Tail Keywords'] = f"✅ {len(long_tail)} keywords"
            print(f"📍 Long Tail Keywords: ✅ {len(long_tail)} keywords")
            print(f"   Examples: {', '.join(long_tail[:3])}")
        else:
            sections_status['Long Tail Keywords'] = "❌ Missing or empty"
            print(f"📍 Long Tail Keywords: ❌ Missing or empty")
        
        # Backend keywords
        if listing.amazon_backend_keywords and len(listing.amazon_backend_keywords.strip()) > 0:
            sections_status['Backend Keywords'] = f"✅ {len(listing.amazon_backend_keywords)} characters"
            print(f"🔧 Backend Keywords: ✅ {len(listing.amazon_backend_keywords)} chars")
            print(f"   Content: {listing.amazon_backend_keywords[:100]}...")
        else:
            sections_status['Backend Keywords'] = "❌ Missing or empty"
            print(f"🔧 Backend Keywords: ❌ Missing or empty")
        
        # 3. Check A+ Content Sections
        print(f"\n🎨 A+ CONTENT SECTIONS:")
        print("-" * 30)
        
        if listing.amazon_aplus_content and len(listing.amazon_aplus_content.strip()) > 0:
            content = listing.amazon_aplus_content.lower()
            aplus_sections = [
                ("Hero Section", "hero"),
                ("Features Section", "features"),
                ("Comparison Section", "comparison"),
                ("Usage Section", "usage"),
                ("Lifestyle Section", "lifestyle"),
                ("A+ Content Suggestions", "suggestions"),
                ("PPC Strategy", "ppc"),
                ("Brand Summary", "brand")
            ]
            
            for section_name, keyword in aplus_sections:
                if keyword in content:
                    sections_status[section_name] = "✅ Present"
                    print(f"   ✅ {section_name}")
                else:
                    sections_status[section_name] = "❌ Missing"
                    print(f"   ❌ {section_name}")
        else:
            sections_status['A+ Content'] = "❌ Missing entirely"
            print(f"   ❌ A+ Content missing entirely")
        
        # 4. Summary
        print(f"\n📊 SECTION SUMMARY:")
        print("=" * 30)
        total_sections = len(sections_status)
        successful_sections = sum(1 for status in sections_status.values() if status.startswith("✅"))
        
        for section, status in sections_status.items():
            print(f"   {section}: {status}")
        
        print(f"\n🎯 OVERALL STATUS: {successful_sections}/{total_sections} sections generated successfully")
        
        if successful_sections < total_sections:
            missing_sections = [section for section, status in sections_status.items() if not status.startswith("✅")]
            print(f"🔧 MISSING SECTIONS: {', '.join(missing_sections)}")
        
        return listing, sections_status
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, {}
    finally:
        # Clean up test product
        product.delete()
        print(f"\n🧹 Cleaned up test product")

if __name__ == "__main__":
    test_keyword_generation()