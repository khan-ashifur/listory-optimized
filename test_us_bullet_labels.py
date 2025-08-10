"""
Test US Market Bullet Labels
Check if bullet labels like "PROFESSIONAL PERFORMANCE:" are working in US market
"""

import os
import sys
import django
import time

# Add the backend directory to the Python path
sys.path.insert(0, r'C:\Users\khana\Desktop\listory-ai\backend')

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "listory.settings")
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from apps.listings.models import GeneratedListing

def test_us_bullet_labels():
    """Test bullet labels in US market"""
    print("🇺🇸 US MARKET BULLET LABEL TEST")
    print("🎯 Testing: Brand tone bullet labels (e.g., 'PROFESSIONAL PERFORMANCE:')")
    print("=" * 70)
    
    try:
        service = ListingGeneratorService()
        
        # Find test product
        product = Product.objects.filter(name__icontains="misting fan").first()
        if not product:
            print("❌ No test product found")
            return
        
        # Configure for US market
        product.marketplace = "com"  # US market
        product.marketplace_language = "en"
        product.brand_tone = "professional"  # Should generate labels like "PROFESSIONAL PERFORMANCE:"
        product.occasion = "none"
        product.save()
        
        print(f"📦 Product: {product.name}")
        print(f"🇺🇸 Market: United States")
        print(f"🎨 Brand Tone: Professional")
        print(f"🎯 Expected Labels: PROFESSIONAL PERFORMANCE:, EXPERT ENGINEERING:, etc.")
        
        print("\n🔄 Generating US listing with brand tone labels...")
        
        # Generate listing
        service.generate_listing(product.id, 'amazon')
        
        # Wait for generation
        print("⏳ Waiting for generation...")
        time.sleep(10)
        
        # Get the latest listing
        listing = GeneratedListing.objects.filter(
            product=product,
            platform='amazon'
        ).order_by('-created_at').first()
        
        if listing and listing.status == 'completed':
            print("✅ Generation completed!")
            
            # Check for bullet labels
            bullets = listing.bullet_points or ""
            bullet_list = bullets.split('\n')
            bullet_list = [b.strip() for b in bullet_list if b.strip()]
            
            print(f"\n📍 BULLET LABEL ANALYSIS:")
            print("=" * 50)
            
            has_labels = []
            expected_labels = ["PROFESSIONAL", "EXPERT", "PROVEN", "INDUSTRY", "PRECISION", "CERTIFIED", "ADVANCED", "TESTED"]
            
            for i, bullet in enumerate(bullet_list[:5], 1):
                print(f"\n   BULLET {i}: {bullet}")
                
                # Check for professional labels
                has_label = any(label in bullet.upper() for label in expected_labels)
                has_colon = ":" in bullet[:30]  # Label should be in first 30 chars
                
                has_labels.append(has_label and has_colon)
                
                if has_label and has_colon:
                    label = bullet.split(':')[0]
                    print(f"   ✅ Label found: '{label}:'")
                else:
                    print(f"   ❌ No professional label found")
            
            # Overall assessment
            labels_percentage = (sum(has_labels) / len(has_labels) * 100) if has_labels else 0
            
            print(f"\n🏆 BULLET LABEL RESULTS:")
            print(f"   Bullets with labels: {sum(has_labels)}/{len(has_labels)}")
            print(f"   Label percentage: {labels_percentage:.1f}%")
            
            if labels_percentage >= 80:
                print(f"   📋 EXCELLENT: Brand tone labels working!")
            elif labels_percentage >= 50:
                print(f"   📋 PARTIAL: Some labels present")
            else:
                print(f"   📋 MISSING: Brand tone labels not working")
                print(f"   🔧 Need to fix brand tone integration")
            
            return labels_percentage >= 50
            
        else:
            print(f"❌ Generation failed: {listing.status if listing else 'Not found'}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_us_bullet_labels()
    print(f"\n🎯 RESULT: {'SUCCESS - Bullet labels working!' if success else 'NEEDS FIX - Labels missing'}")