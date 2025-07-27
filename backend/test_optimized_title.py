#!/usr/bin/env python3
"""
Test the optimized title generation with Amazon SEO requirements.
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

def test_optimized_title():
    """Test optimized title generation with Amazon SEO requirements."""
    print("🎯 TESTING OPTIMIZED AMAZON TITLE GENERATION")
    print("=" * 60)
    
    # Get or create user
    user, _ = User.objects.get_or_create(username='testuser', defaults={'email': 'test@example.com'})
    
    # Create test product
    product = Product.objects.create(
        name='Wireless Bluetooth Gaming Headset with Microphone',
        user=user,
        description='Premium gaming headset with 7.1 surround sound, noise-canceling microphone, RGB lighting, and comfortable design for PC, PS5, Xbox gaming.',
        brand_name='GameMax',
        brand_tone='casual',
        target_platform='amazon',
        price=89.99,
        categories='Electronics, Gaming Accessories, Gaming Headsets',
        features='7.1 surround sound, noise-canceling microphone, RGB lighting, comfortable padding, 20-hour battery, universal compatibility',
        target_keywords='gaming headset, wireless headset, bluetooth gaming, microphone',
        seo_keywords='gaming headset with microphone, wireless gaming headphones, RGB gaming headset',
        long_tail_keywords='wireless gaming headset with microphone for PC PS5 Xbox',
        faqs='Q: Compatible with PS5? A: Yes, works with PC, PS5, Xbox. Q: Battery life? A: Up to 20 hours.',
        whats_in_box='Gaming headset, USB receiver, charging cable, user manual',
        competitor_urls='https://www.amazon.com/competitor-gaming-headset'
    )
    
    print(f"✅ Created test product: {product.name}")
    print(f"🏷️  Brand: {product.brand_name}")
    
    # Generate listing
    generator = ListingGeneratorService()
    print("\n🚀 Generating listing with optimized title prompt...")
    
    try:
        listing = generator.generate_listing(product.id, 'amazon')
        
        print("\n📊 TITLE OPTIMIZATION ANALYSIS:")
        print("=" * 50)
        
        if not listing.title:
            print("❌ No title generated")
            return False
        
        title = listing.title
        title_length = len(title)
        
        print(f"📝 GENERATED TITLE:")
        print(f"   '{title}'")
        print(f"   Length: {title_length} characters")
        
        # Check Amazon optimization requirements
        print(f"\n🔍 AMAZON OPTIMIZATION CHECK:")
        print("-" * 35)
        
        # 1. Length check (150-200 characters optimal for Amazon)
        length_status = "✅" if 150 <= title_length <= 200 else "⚠️" if 120 <= title_length < 150 else "❌"
        print(f"   Length: {length_status} {title_length}/150-200 chars (Amazon optimal)")
        
        # 2. Brand name check
        brand_included = product.brand_name.lower() in title.lower()
        brand_at_start = title.lower().startswith(product.brand_name.lower())
        brand_status = "✅" if brand_at_start else "⚠️" if brand_included else "❌"
        print(f"   Brand Name: {brand_status} {'At start' if brand_at_start else 'Included' if brand_included else 'Missing'}")
        
        # 3. SEO keywords check
        seo_keywords = ['gaming', 'headset', 'wireless', 'bluetooth', 'microphone']
        keyword_count = sum(1 for keyword in seo_keywords if keyword.lower() in title.lower())
        keyword_status = "✅" if keyword_count >= 4 else "⚠️" if keyword_count >= 3 else "❌"
        print(f"   SEO Keywords: {keyword_status} {keyword_count}/{len(seo_keywords)} keywords found")
        
        # 4. Product type clarity
        product_types = ['headset', 'headphones', 'gaming']
        product_type_found = any(ptype.lower() in title.lower() for ptype in product_types)
        product_status = "✅" if product_type_found else "❌"
        print(f"   Product Type: {product_status} {'Clear product category' if product_type_found else 'Unclear category'}")
        
        # 5. Features/benefits
        key_features = ['surround', 'noise', 'rgb', 'battery', 'compatible', 'comfort']
        feature_count = sum(1 for feature in key_features if feature.lower() in title.lower())
        feature_status = "✅" if feature_count >= 2 else "⚠️" if feature_count >= 1 else "❌"
        print(f"   Key Features: {feature_status} {feature_count} features mentioned")
        
        # 6. Emotional appeal check
        emotional_words = ['premium', 'ultimate', 'professional', 'advanced', 'superior', 'experience', 'perfect', 'studio-quality']
        emotional_count = sum(1 for word in emotional_words if word.lower() in title.lower())
        emotional_status = "✅" if emotional_count >= 1 else "❌"
        print(f"   Emotional Hook: {emotional_status} {emotional_count} emotional words found")
        
        # Overall assessment
        print(f"\n🎯 OVERALL TITLE ASSESSMENT:")
        print("-" * 35)
        
        requirements_met = 0
        total_requirements = 6
        
        if length_status == "✅": requirements_met += 1
        if brand_status in ["✅", "⚠️"]: requirements_met += 1
        if keyword_status in ["✅", "⚠️"]: requirements_met += 1
        if product_status == "✅": requirements_met += 1
        if feature_status in ["✅", "⚠️"]: requirements_met += 1
        if emotional_status == "✅": requirements_met += 1
        
        success_rate = (requirements_met / total_requirements) * 100
        
        if success_rate >= 85:
            overall_status = "✅ EXCELLENT"
        elif success_rate >= 70:
            overall_status = "⚠️ GOOD"
        else:
            overall_status = "❌ NEEDS IMPROVEMENT"
        
        print(f"   Status: {overall_status}")
        print(f"   Score: {requirements_met}/{total_requirements} requirements met ({success_rate:.0f}%)")
        
        # Provide specific improvements if needed
        if success_rate < 85:
            print(f"\n💡 IMPROVEMENT SUGGESTIONS:")
            if length_status == "❌":
                print(f"   • Expand title to 150-200 characters for better Amazon visibility")
            if brand_status == "❌":
                print(f"   • Include brand name '{product.brand_name}' at the beginning")
            if keyword_status != "✅":
                print(f"   • Add more SEO keywords: {[k for k in seo_keywords if k.lower() not in title.lower()]}")
            if feature_status != "✅":
                print(f"   • Mention more key features (surround sound, RGB, battery life, etc.)")
            if emotional_status == "❌":
                print(f"   • Add emotional hook words (premium, ultimate, experience, etc.)")
        
        print(f"\n🔍 KEYWORD ANALYSIS (kept for reference):")
        if listing.keywords:
            all_keywords = [k.strip() for k in listing.keywords.split(',') if k.strip()]
            short_tail = [k for k in all_keywords if len(k.split()) <= 2]
            long_tail = [k for k in all_keywords if len(k.split()) > 2]
            print(f"   Total Keywords: {len(all_keywords)} ({len(short_tail)} short + {len(long_tail)} long)")
        
        return success_rate >= 85
        
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
    success = test_optimized_title()
    if success:
        print(f"\n🎉 TITLE OPTIMIZATION SUCCESS!")
    else:
        print(f"\n🔧 TITLE NEEDS FURTHER OPTIMIZATION")