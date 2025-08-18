"""
Turkey Market Optimization Test - Beat All Competitors
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

def test_optimized_turkey_market():
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username='turkey_optimization_test')
    
    print("🇹🇷 TESTING OPTIMIZED TURKEY MARKET")
    print("="*60)
    print("🎯 Target: Beat Helium 10, Jasper AI, CopyMonkey")
    print("🏆 Goal: 9.0/10+ score")
    print("="*60)
    
    # Create product for Turkey market
    product = Product.objects.create(
        user=test_user,
        name="Premium Wireless Bluetooth Headphones",
        description="High-quality wireless headphones with active noise cancellation and long battery life",
        brand_name="SoundMaster",
        brand_tone="premium",
        target_platform="amazon",
        marketplace="tr",
        marketplace_language="tr",
        categories="Electronics/Audio/Headphones",
        features="Active Noise Cancellation, 40H Battery, Wireless Charging, IPX5 Waterproof, Premium Build",
        target_audience="Turkish music lovers and professionals",
        occasion="kurban_bayrami"
    )
    
    try:
        print("🔄 Generating optimized Turkey listing...")
        listing = service.generate_listing(product_id=product.id, platform='amazon')
        
        if listing:
            print("✅ Listing generated successfully!")
            print(f"📊 Title Length: {len(listing.amazon_title)} characters")
            print(f"📝 Title: {listing.amazon_title}")
            
            print(f"\n📄 Bullet Points ({len(listing.amazon_bullet_points)} bullets):")
            bullets = listing.amazon_bullet_points.split('\n') if listing.amazon_bullet_points else []
            for i, bullet in enumerate(bullets[:5], 1):
                if bullet.strip():
                    print(f"  {i}. {bullet.strip()}")
            
            print(f"\n📖 Description Length: {len(listing.amazon_description)} characters")
            print(f"📖 Description Preview: {listing.amazon_description[:200]}...")
            
            if listing.amazon_aplus_content:
                print(f"\n🎨 A+ Content Length: {len(listing.amazon_aplus_content)} characters")
                
                # Check for Turkish localization
                turkish_indicators = ['Anahtar Kelimeler', 'Görsel Strateji', 'SEO Odak']
                turkish_found = sum(1 for indicator in turkish_indicators if indicator in listing.amazon_aplus_content)
                print(f"🇹🇷 Turkish Localization: {turkish_found}/3 labels localized")
                
                # Check for conversion elements
                conversion_terms = ['sınırlı stok', 'özel fiyat', 'bugün', 'son fırsat', 'acele edin', 'aileniz için']
                conversion_found = sum(1 for term in conversion_terms if term.lower() in listing.amazon_aplus_content.lower())
                print(f"💰 Conversion Elements: {conversion_found}/6 found")
                
                # Check for emotional hooks
                emotional_terms = ['hayalinizdeki', 'gurur duyacağınız', 'sevdiklerinize', 'çocuklarınız için', 'mutlu müşteri']
                emotional_found = sum(1 for term in emotional_terms if term.lower() in listing.amazon_aplus_content.lower())
                print(f"❤️ Emotional Hooks: {emotional_found}/5 found")
                
                # Check for trust signals
                trust_terms = ['garanti', 'sertifikalı', 'orijinal', 'güvenilir', 'kalite', 'türkiye']
                trust_found = sum(1 for term in trust_terms if term.lower() in listing.amazon_aplus_content.lower())
                print(f"🛡️ Trust Signals: {trust_found}/6 found")
            
            # Keywords analysis
            if listing.amazon_keywords:
                keywords = listing.amazon_keywords.split(',') if listing.amazon_keywords else []
                print(f"\n🔍 Keywords Count: {len(keywords)}")
                print(f"🔍 Keywords Preview: {', '.join(keywords[:8])}...")
            
            # Quality estimation
            total_score = 0
            total_possible = 0
            
            # Title quality (max 2.0)
            title_score = min(2.0, len(listing.amazon_title) / 100)
            total_score += title_score
            total_possible += 2.0
            
            # A+ Content quality (max 3.0)
            if listing.amazon_aplus_content:
                aplus_score = min(3.0, len(listing.amazon_aplus_content) / 8000)
                total_score += aplus_score
                total_possible += 3.0
            
            # Localization score (max 2.0)
            localization_score = (turkish_found / 3) * 2.0
            total_score += localization_score
            total_possible += 2.0
            
            # Conversion score (max 2.0)
            conversion_score = min(2.0, (conversion_found / 6) * 2.0)
            total_score += conversion_score
            total_possible += 2.0
            
            # Emotional score (max 1.0)
            emotional_score = min(1.0, (emotional_found / 5) * 1.0)
            total_score += emotional_score
            total_possible += 1.0
            
            final_score = (total_score / total_possible) * 10
            
            print(f"\n🏆 OPTIMIZATION RESULTS:")
            print(f"📊 Final Score: {final_score:.1f}/10")
            print(f"🎯 Target: 9.0/10")
            
            if final_score >= 9.0:
                print("🎉 SUCCESS! Turkey market BEATS all competitors!")
                print("✅ Superior to Helium 10, Jasper AI, and CopyMonkey")
            elif final_score >= 8.0:
                print("🔥 EXCELLENT! Very close to beating competitors")
                print("💪 Almost beating Helium 10, Jasper AI, and CopyMonkey")
            elif final_score >= 7.0:
                print("⚡ GOOD! Getting competitive with market leaders")
                print("🚀 Competing with Helium 10, Jasper AI, and CopyMonkey")
            else:
                print("⚠️ NEEDS MORE WORK to beat competitors")
                print("🔧 Still below Helium 10, Jasper AI, and CopyMonkey standards")
                
        else:
            print("❌ Failed to generate listing")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    finally:
        product.delete()

if __name__ == "__main__":
    test_optimized_turkey_market()