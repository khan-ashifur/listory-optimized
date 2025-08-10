"""
Test German Bullet Labels
Check if German bullets now have proper brand tone labels in German
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

def test_german_bullet_labels():
    """Test German bullet labels with brand tone"""
    print("🇩🇪 GERMAN BULLET LABELS TEST")
    print("🎯 Testing: German brand tone labels (e.g., 'PROFESSIONELLE LEISTUNG:')")
    print("=" * 70)
    
    try:
        service = ListingGeneratorService()
        
        # Find test product
        product = Product.objects.filter(name__icontains="misting fan").first()
        if not product:
            print("❌ No test product found")
            return
        
        # Configure for German market with professional tone
        product.marketplace = "de"
        product.marketplace_language = "de"
        product.brand_tone = "professional"  # Should generate German professional labels
        product.occasion = "none"
        product.save()
        
        print(f"📦 Product: {product.name}")
        print(f"🇩🇪 Market: Germany") 
        print(f"🎨 Brand Tone: Professional")
        print(f"🎯 Expected Labels: PROFESSIONELLE LEISTUNG:, BEWÄHRTE QUALITÄT:, etc.")
        
        print("\n🔄 Generating German listing with brand tone labels...")
        
        # Generate listing
        service.generate_listing(product.id, 'amazon')
        
        # Wait for generation
        print("⏳ Waiting for generation...")
        time.sleep(12)
        
        # Get the latest listing
        listing = GeneratedListing.objects.filter(
            product=product,
            platform='amazon'
        ).order_by('-created_at').first()
        
        if listing and listing.status == 'completed':
            print("✅ Generation completed!")
            
            # Check for German bullet labels
            bullets = listing.bullet_points or ""
            bullet_list = bullets.split('\n')
            bullet_list = [b.strip() for b in bullet_list if b.strip()]
            
            print(f"\n📍 GERMAN BULLET LABEL ANALYSIS:")
            print("=" * 50)
            
            has_labels = []
            german_professional_labels = [
                "PROFESSIONELLE", "BEWÄHRTE", "ZERTIFIZIERTE", "EXPERT", "QUALITÄT", 
                "LEISTUNG", "PRÄZISION", "GEPRÜFTE", "HOCHWERTIGE", "INDUSTRIELL"
            ]
            
            for i, bullet in enumerate(bullet_list[:5], 1):
                print(f"\n   BULLET {i}: {bullet[:100]}...")
                
                # Check for German professional labels  
                has_german_label = any(label in bullet.upper() for label in german_professional_labels)
                has_colon = ":" in bullet[:40]  # Label should be in first 40 chars
                
                # Check for emotional hook
                has_emotional_hook = "wie ein profi" in bullet.lower() and "ganz ohne" in bullet.lower()
                
                has_labels.append(has_german_label and has_colon)
                
                if has_german_label and has_colon:
                    label = bullet.split(':')[0]
                    print(f"   ✅ German label found: '{label}:'")
                else:
                    print(f"   ❌ No German brand label found")
                
                if has_emotional_hook:
                    print(f"   ✅ Emotional hook: 'wie ein Profi – ganz ohne' present")
                else:
                    print(f"   ⚠️ Emotional hook: Missing or incomplete")
            
            # Overall assessment
            labels_percentage = (sum(has_labels) / len(has_labels) * 100) if has_labels else 0
            
            # Check umlauts
            german_chars = ['ä', 'ö', 'ü', 'ß', 'Ä', 'Ö', 'Ü']
            total_umlauts = sum(bullets.count(char) for char in german_chars)
            
            print(f"\n🏆 GERMAN BULLET LABEL RESULTS:")
            print(f"   Bullets with German labels: {sum(has_labels)}/{len(has_labels)}")
            print(f"   Label percentage: {labels_percentage:.1f}%")
            print(f"   Total umlauts preserved: {total_umlauts}")
            
            if labels_percentage >= 80 and total_umlauts >= 10:
                print(f"   🎯 PERFECT: German brand labels + umlauts working!")
            elif labels_percentage >= 50:
                print(f"   📋 GOOD: Partial German labels present")
            else:
                print(f"   📋 NEEDS WORK: German brand labels missing")
            
            return labels_percentage >= 50 and total_umlauts >= 10
            
        else:
            print(f"❌ Generation failed: {listing.status if listing else 'Not found'}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_german_bullet_labels()
    print(f"\n🎯 RESULT: {'SUCCESS - German bullet labels restored!' if success else 'NEEDS MORE WORK'}")