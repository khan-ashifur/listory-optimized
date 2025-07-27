#!/usr/bin/env python3
"""
Test the restored format with proper keyword counts and bullet labels.
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

def test_restored_format():
    """Test restored format with proper keyword counts and bullet labels."""
    print("🧪 TESTING RESTORED FORMAT - LABELS & KEYWORD COUNTS")
    print("=" * 60)
    
    # Get or create user
    user, _ = User.objects.get_or_create(username='testuser', defaults={'email': 'test@example.com'})
    
    # Create test product
    product = Product.objects.create(
        name='Wireless Noise Cancelling Bluetooth Headphones Pro',
        user=user,
        description='Premium wireless headphones with active noise cancellation, 30-hour battery life, premium sound quality, comfortable over-ear design, and quick charge technology.',
        brand_name='AudioMax',
        brand_tone='professional',
        target_platform='amazon',
        price=149.99,
        categories='Electronics, Headphones, Wireless Headphones, Noise Cancelling',
        features='Active noise cancellation, 30-hour battery, wireless bluetooth 5.0, premium drivers, comfortable padding, quick charge, foldable design, carrying case',
        target_keywords='wireless headphones, bluetooth headphones, noise cancelling headphones',
        seo_keywords='best wireless headphones 2024, premium bluetooth headphones, noise cancelling headphones',
        long_tail_keywords='wireless noise cancelling headphones for travel, best bluetooth headphones for music',
        faqs='Q: How long does battery last? A: Up to 30 hours. Q: Do they work with iPhone? A: Yes, compatible with all devices.',
        whats_in_box='Headphones, carrying case, charging cable, 3.5mm cable, user manual',
        competitor_urls='https://www.amazon.com/competitor-headphones'
    )
    
    print(f"✅ Created test product: {product.name}")
    
    # Generate listing
    generator = ListingGeneratorService()
    print("\n🚀 Generating listing with restored format...")
    
    try:
        listing = generator.generate_listing(product.id, 'amazon')
        
        print("\n📊 DETAILED FORMAT ANALYSIS:")
        print("=" * 50)
        
        # 1. Check bullet point format
        print("🔸 BULLET POINT FORMAT CHECK:")
        print("-" * 35)
        if listing.bullet_points:
            bullets = [b.strip() for b in listing.bullet_points.split('\n\n') if b.strip()]
            print(f"Total bullets: {len(bullets)}")
            
            for i, bullet in enumerate(bullets, 1):
                has_label = ':' in bullet and bullet.split(':')[0].isupper()
                label_status = "✅" if has_label else "❌"
                label = bullet.split(':')[0] if ':' in bullet else "No label"
                content_length = len(bullet)
                
                print(f"  Bullet {i}: {label_status} Label format")
                print(f"    Label: {label}")
                print(f"    Length: {content_length} chars")
                print(f"    Preview: {bullet[:80]}...")
                print()
        else:
            print("❌ No bullet points found")
        
        # 2. Check keyword distribution
        print("🔑 KEYWORD DISTRIBUTION CHECK:")
        print("-" * 35)
        
        if listing.keywords:
            all_keywords = [k.strip() for k in listing.keywords.split(',') if k.strip()]
            
            short_tail = [k for k in all_keywords if len(k.split()) <= 2]
            long_tail = [k for k in all_keywords if len(k.split()) > 2]
            
            print(f"📊 TOTAL KEYWORDS: {len(all_keywords)}")
            print(f"📌 SHORT-TAIL (≤2 words): {len(short_tail)}")
            print(f"📍 LONG-TAIL (>2 words): {len(long_tail)}")
            
            # Check targets
            short_target = "10+"
            long_target = "20+"
            short_status = "✅" if len(short_tail) >= 10 else "⚠️" if len(short_tail) >= 8 else "❌"
            long_status = "✅" if len(long_tail) >= 20 else "⚠️" if len(long_tail) >= 15 else "❌"
            
            print(f"\n🎯 TARGET COMPARISON:")
            print(f"  Short-tail: {short_status} {len(short_tail)}/{short_target} (target)")
            print(f"  Long-tail:  {long_status} {len(long_tail)}/{long_target} (target)")
            
            print(f"\n📌 SHORT-TAIL EXAMPLES:")
            for keyword in short_tail[:5]:
                print(f"    • {keyword} ({len(keyword.split())} words)")
            
            print(f"\n📍 LONG-TAIL EXAMPLES:")
            for keyword in long_tail[:5]:
                print(f"    • {keyword} ({len(keyword.split())} words)")
        
        # 3. Check backend keywords
        print(f"\n🔧 BACKEND KEYWORDS CHECK:")
        print("-" * 30)
        if listing.amazon_backend_keywords:
            backend_length = len(listing.amazon_backend_keywords)
            backend_count = len([k.strip() for k in listing.amazon_backend_keywords.split(',') if k.strip()])
            backend_status = "✅" if backend_length >= 240 else "⚠️" if backend_length >= 200 else "❌"
            
            print(f"  Length: {backend_status} {backend_length}/240+ chars (target)")
            print(f"  Count: {backend_count} terms")
            print(f"  Preview: {listing.amazon_backend_keywords[:100]}...")
        else:
            print("  ❌ No backend keywords found")
        
        # 4. Overall assessment
        print(f"\n🎯 OVERALL ASSESSMENT:")
        print("=" * 30)
        
        bullet_format_ok = listing.bullet_points and ':' in listing.bullet_points
        short_keywords_ok = listing.keywords and len([k for k in listing.keywords.split(',') if len(k.strip().split()) <= 2]) >= 8
        long_keywords_ok = listing.keywords and len([k for k in listing.keywords.split(',') if len(k.strip().split()) > 2]) >= 15
        backend_ok = listing.amazon_backend_keywords and len(listing.amazon_backend_keywords) >= 200
        
        print(f"  Bullet Labels: {'✅' if bullet_format_ok else '❌'}")
        print(f"  Short Keywords: {'✅' if short_keywords_ok else '❌'}")
        print(f"  Long Keywords: {'✅' if long_keywords_ok else '❌'}")
        print(f"  Backend Keywords: {'✅' if backend_ok else '❌'}")
        
        success = bullet_format_ok and short_keywords_ok and long_keywords_ok and backend_ok
        
        if success:
            print(f"\n🎉 SUCCESS: All format requirements met!")
        else:
            print(f"\n⚠️ PARTIAL: Some requirements need adjustment")
        
        return listing, success
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, False
    finally:
        # Clean up test product
        product.delete()
        print(f"\n🧹 Cleaned up test product")

if __name__ == "__main__":
    test_restored_format()