#!/usr/bin/env python3
"""
Test the updated keyword distribution with new prompt.
"""
import os
import sys
import django

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from django.contrib.auth.models import User

def test_keyword_distribution():
    """Test updated keyword distribution with new prompt."""
    print("🧪 TESTING UPDATED KEYWORD DISTRIBUTION")
    print("=" * 60)
    
    # Get or create user
    user, _ = User.objects.get_or_create(username='testuser', defaults={'email': 'test@example.com'})
    
    # Create test product
    product = Product.objects.create(
        name='Professional Gaming Headset with Microphone',
        user=user,
        description='High-quality gaming headset with noise-canceling microphone, surround sound, comfortable padding, and RGB lighting for PC, PS5, Xbox gaming.',
        brand_name='GameSound',
        brand_tone='casual',
        target_platform='amazon',
        price=79.99,
        categories='Electronics, Gaming Accessories, Gaming Headsets',
        features='Noise-canceling microphone, 7.1 surround sound, RGB lighting, comfortable padding, detachable cable, universal compatibility',
        target_keywords='gaming headset, microphone, headphones, gaming audio',
        seo_keywords='gaming headset with microphone, professional gaming headphones, RGB gaming headset',
        long_tail_keywords='gaming headset with noise canceling microphone for PC',
        faqs='Q: Compatible with PS5? A: Yes, works with PC, PS5, Xbox, and mobile. Q: Is microphone detachable? A: Yes, fully detachable.',
        whats_in_box='Gaming headset, detachable microphone, USB cable, 3.5mm cable, user manual',
        competitor_urls='https://www.amazon.com/competitor-gaming-headset'
    )
    
    print(f"✅ Created test product: {product.name}")
    
    # Generate listing
    generator = ListingGeneratorService()
    print("\n🚀 Generating listing with updated keyword prompt...")
    
    try:
        listing = generator.generate_listing(product.id, 'amazon')
        
        print("\n🔍 KEYWORD DISTRIBUTION ANALYSIS:")
        print("=" * 50)
        
        if not listing.keywords:
            print("❌ No keywords generated")
            return
        
        # Analyze keyword distribution
        all_keywords = [k.strip() for k in listing.keywords.split(',') if k.strip()]
        
        short_tail = []  # <= 2 words
        long_tail = []   # > 2 words
        
        for keyword in all_keywords:
            word_count = len(keyword.split())
            if word_count <= 2:
                short_tail.append(keyword)
            else:
                long_tail.append(keyword)
        
        print(f"📊 TOTAL KEYWORDS: {len(all_keywords)}")
        print(f"📌 SHORT-TAIL (≤2 words): {len(short_tail)}")
        print(f"📍 LONG-TAIL (>2 words): {len(long_tail)}")
        
        # Check if we meet the target distribution
        target_short = 8
        target_long = 12
        
        print(f"\n🎯 TARGET vs ACTUAL:")
        print("-" * 25)
        short_status = "✅" if len(short_tail) >= target_short else "❌"
        long_status = "✅" if len(long_tail) >= target_long else "❌"
        
        print(f"Short-tail: {short_status} {len(short_tail)}/{target_short}+ (target)")
        print(f"Long-tail:  {long_status} {len(long_tail)}/{target_long}+ (target)")
        
        print(f"\n📌 SHORT-TAIL KEYWORDS ({len(short_tail)}):")
        print("-" * 30)
        if short_tail:
            for i, keyword in enumerate(short_tail, 1):
                word_count = len(keyword.split())
                print(f"{i:2d}. {keyword} ({word_count} words)")
        else:
            print("❌ NO SHORT-TAIL KEYWORDS!")
        
        print(f"\n📍 LONG-TAIL KEYWORDS ({len(long_tail)}):")
        print("-" * 30)
        for i, keyword in enumerate(long_tail[:8], 1):  # Show first 8
            word_count = len(keyword.split())
            print(f"{i:2d}. {keyword} ({word_count} words)")
        if len(long_tail) > 8:
            print(f"    ... and {len(long_tail) - 8} more")
        
        # Frontend simulation
        print(f"\n💻 FRONTEND SIMULATION:")
        print("-" * 25)
        print(f"User will see:")
        print(f"• Short-tail section: {len(short_tail)} keywords")
        print(f"• Long-tail section: {len(long_tail)} keywords")
        
        if len(short_tail) >= target_short:
            print(f"✅ SUCCESS: User will see {len(short_tail)} short-tail keywords!")
        else:
            print(f"❌ ISSUE: User still sees only {len(short_tail)} short-tail keywords")
        
        return listing, len(short_tail), len(long_tail)
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, 0, 0
    finally:
        # Clean up test product
        product.delete()
        print(f"\n🧹 Cleaned up test product")

if __name__ == "__main__":
    test_keyword_distribution()