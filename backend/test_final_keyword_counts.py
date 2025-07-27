#!/usr/bin/env python3
"""
Test final keyword counts with updated requirements.
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

def test_final_keyword_counts():
    """Test final keyword counts with updated requirements."""
    print("🎯 FINAL KEYWORD COUNT TEST - TARGET: 35+ KEYWORDS")
    print("=" * 60)
    
    # Get or create user
    user, _ = User.objects.get_or_create(username='testuser', defaults={'email': 'test@example.com'})
    
    # Create test product
    product = Product.objects.create(
        name='Smart Fitness Tracker Watch with Heart Rate Monitor',
        user=user,
        description='Advanced fitness tracker with heart rate monitoring, GPS, sleep tracking, waterproof design, and smartphone notifications. Perfect for runners, athletes, and health enthusiasts.',
        brand_name='FitPro',
        brand_tone='casual',
        target_platform='amazon',
        price=99.99,
        categories='Sports & Outdoors, Fitness Trackers, Smartwatches',
        features='Heart rate monitor, GPS tracking, sleep analysis, waterproof IPX7, 7-day battery, smartphone sync, multiple sport modes',
        target_keywords='fitness tracker, smartwatch, heart rate monitor, GPS watch',
        seo_keywords='fitness tracker with GPS, waterproof smartwatch, heart rate monitor watch',
        long_tail_keywords='fitness tracker with heart rate and GPS for running',
        faqs='Q: Is it waterproof? A: Yes, IPX7 rated. Q: Battery life? A: Up to 7 days.',
        whats_in_box='Fitness tracker, charging cable, user manual, warranty card',
        competitor_urls='https://www.amazon.com/competitor-fitness-tracker'
    )
    
    print(f"✅ Created test product: {product.name}")
    
    # Generate listing
    generator = ListingGeneratorService()
    print("\n🚀 Generating listing with enhanced keyword requirements...")
    
    try:
        listing = generator.generate_listing(product.id, 'amazon')
        
        print("\n📊 FINAL KEYWORD COUNT ANALYSIS:")
        print("=" * 50)
        
        if not listing.keywords:
            print("❌ No keywords generated")
            return False
        
        # Analyze keyword distribution
        all_keywords = [k.strip() for k in listing.keywords.split(',') if k.strip()]
        
        short_tail = [k for k in all_keywords if len(k.split()) <= 2]
        long_tail = [k for k in all_keywords if len(k.split()) > 2]
        
        print(f"📊 KEYWORD BREAKDOWN:")
        print(f"   Total Keywords: {len(all_keywords)}")
        print(f"   Short-tail (≤2 words): {len(short_tail)}")
        print(f"   Long-tail (>2 words): {len(long_tail)}")
        
        # Check targets
        short_target_min = 10
        short_target_max = 12
        long_target = 25
        total_target = 35
        
        print(f"\n🎯 TARGET COMPARISON:")
        short_status = "✅" if short_target_min <= len(short_tail) <= short_target_max else "❌"
        long_status = "✅" if len(long_tail) >= long_target else "❌"
        total_status = "✅" if len(all_keywords) >= total_target else "❌"
        
        print(f"   Short-tail: {short_status} {len(short_tail)}/{short_target_min}-{short_target_max} (target)")
        print(f"   Long-tail:  {long_status} {len(long_tail)}/{long_target}+ (target)")
        print(f"   Total:      {total_status} {len(all_keywords)}/{total_target}+ (target)")
        
        # Backend keywords
        backend_length = len(listing.amazon_backend_keywords) if listing.amazon_backend_keywords else 0
        backend_status = "✅" if backend_length >= 240 else "❌"
        print(f"   Backend:    {backend_status} {backend_length}/240+ chars")
        
        # Show keyword examples
        print(f"\n📌 SHORT-TAIL KEYWORDS ({len(short_tail)}):")
        for i, keyword in enumerate(short_tail, 1):
            print(f"   {i:2d}. {keyword} ({len(keyword.split())} words)")
        
        print(f"\n📍 LONG-TAIL KEYWORDS ({len(long_tail)}) - First 10:")
        for i, keyword in enumerate(long_tail[:10], 1):
            print(f"   {i:2d}. {keyword} ({len(keyword.split())} words)")
        if len(long_tail) > 10:
            print(f"   ... and {len(long_tail) - 10} more")
        
        # Check bullet format
        print(f"\n🔸 BULLET POINT FORMAT:")
        if listing.bullet_points:
            bullets = [b.strip() for b in listing.bullet_points.split('\n\n') if b.strip()]
            label_count = sum(1 for bullet in bullets if ':' in bullet and bullet.split(':')[0].isupper())
            bullet_status = "✅" if label_count >= 4 else "❌"
            print(f"   Format: {bullet_status} {label_count}/{len(bullets)} bullets have LABEL: format")
        else:
            print(f"   Format: ❌ No bullets found")
        
        # Overall success check
        all_targets_met = (
            short_target_min <= len(short_tail) <= short_target_max and
            len(long_tail) >= long_target and
            len(all_keywords) >= total_target and
            backend_length >= 240
        )
        
        print(f"\n🏆 FINAL RESULT:")
        if all_targets_met:
            print(f"   ✅ SUCCESS: All keyword targets met!")
            print(f"   📊 Frontend will show: {len(short_tail)} short-tail, {len(long_tail)} long-tail")
            print(f"   🎯 User will see proper keyword distribution")
        else:
            print(f"   ⚠️ PARTIAL: Some targets still need adjustment")
        
        return all_targets_met
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Clean up test product
        product.delete()
        print(f"\n🧹 Cleaned up test product")

if __name__ == "__main__":
    success = test_final_keyword_counts()
    if success:
        print(f"\n🎉 ALL REQUIREMENTS MET - SYSTEM READY!")
    else:
        print(f"\n🔧 SOME ADJUSTMENTS STILL NEEDED")