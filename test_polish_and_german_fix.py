"""
Test Polish Language Support and German Bullet Point Fix
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

def test_polish_language():
    """Test Polish language generation"""
    print("🇵🇱 TESTING POLISH LANGUAGE SUPPORT")
    print("=" * 60)
    
    try:
        service = ListingGeneratorService()
        
        # Find test product
        product = Product.objects.filter(name__icontains="misting fan").first()
        if not product:
            print("❌ No test product found")
            return False
        
        # Configure for Polish market
        product.marketplace = "pl"
        product.marketplace_language = "pl"
        product.brand_tone = "casual"
        product.occasion = "Christmas"
        product.save()
        
        print(f"📦 Product: {product.name}")
        print(f"🇵🇱 Market: Poland (pl)")
        print(f"🎄 Occasion: Christmas")
        
        print("\n🔄 Generating Polish listing...")
        
        # Generate listing
        service.generate_listing(product.id, 'amazon')
        
        # Wait for generation
        print("⏳ Waiting...")
        time.sleep(8)
        
        # Get the listing
        listing = GeneratedListing.objects.filter(
            product=product,
            platform='amazon'
        ).order_by('-created_at').first()
        
        if listing and listing.status == 'completed':
            print("✅ Polish generation completed!")
            
            # Check Polish characters
            title = listing.title or ""
            bullets = listing.bullet_points or ""
            total_text = title + bullets
            
            print(f"\n📌 TITLE: {title[:100]}...")
            
            # Check for Polish special characters
            polish_chars = ['ą', 'ć', 'ę', 'ł', 'ń', 'ó', 'ś', 'ź', 'ż', 'Ą', 'Ć', 'Ę', 'Ł', 'Ń', 'Ó', 'Ś', 'Ź', 'Ż']
            polish_count = sum(total_text.count(char) for char in polish_chars)
            
            print(f"🔤 Polish characters found: {polish_count}")
            
            # Check for Polish words
            polish_words = ['wreszcie', 'idealny', 'wygodny', 'łatwy', 'więcej', 'jakość']
            polish_words_found = sum(word in total_text.lower() for word in polish_words)
            
            print(f"📝 Polish words found: {polish_words_found}/6")
            
            # Check bullets
            bullet_list = bullets.split('\n')[:2]
            print(f"\n📍 First bullet: {bullet_list[0][:80]}..." if bullet_list else "No bullets")
            
            success = polish_count > 0 and polish_words_found >= 2
            print(f"🏆 Polish test: {'✅ PASS' if success else '❌ FAIL'}")
            return success
            
        else:
            print("❌ Polish generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Polish test error: {e}")
        return False

def test_german_bullet_fix():
    """Test German bullet point umlaut preservation"""
    print("\n🇩🇪 TESTING GERMAN BULLET UMLAUT FIX")
    print("=" * 60)
    
    try:
        service = ListingGeneratorService()
        
        # Find test product
        product = Product.objects.filter(name__icontains="misting fan").first()
        if not product:
            print("❌ No test product found")
            return False
        
        # Configure for German market
        product.marketplace = "de"
        product.marketplace_language = "de"
        product.brand_tone = "casual"
        product.occasion = "none"
        product.save()
        
        print(f"📦 Product: {product.name}")
        print(f"🇩🇪 Market: Germany")
        
        print("\n🔄 Generating German listing with fixed bullets...")
        
        # Generate listing
        service.generate_listing(product.id, 'amazon')
        
        # Wait for generation
        print("⏳ Waiting...")
        time.sleep(8)
        
        # Get the listing
        listing = GeneratedListing.objects.filter(
            product=product,
            platform='amazon'
        ).order_by('-created_at').first()
        
        if listing and listing.status == 'completed':
            print("✅ German generation completed!")
            
            # Check bullet points specifically
            bullets = listing.bullet_points or ""
            title = listing.title or ""
            
            print(f"\n📌 TITLE umlauts: {title[:100]}...")
            
            # Count umlauts in bullets
            german_chars = ['ä', 'ö', 'ü', 'ß', 'Ä', 'Ö', 'Ü']
            bullet_umlauts = sum(bullets.count(char) for char in german_chars)
            title_umlauts = sum(title.count(char) for char in german_chars)
            
            print(f"🔤 Title umlauts: {title_umlauts}")
            print(f"🔤 Bullet umlauts: {bullet_umlauts}")
            
            # Show bullet samples
            bullet_list = bullets.split('\n\n')[:3]
            print(f"\n📍 BULLET SAMPLES:")
            for i, bullet in enumerate(bullet_list, 1):
                if bullet.strip():
                    print(f"   {i}. {bullet.strip()[:80]}...")
                    bullet_has_umlauts = any(char in bullet for char in german_chars)
                    print(f"      Has umlauts: {'✅' if bullet_has_umlauts else '❌'}")
            
            # Check for problem patterns
            problems = []
            if 'fr ' in bullets and 'für' not in bullets:
                problems.append("'fr' without 'für'")
            if 'grere' in bullets:
                problems.append("'grere' should be 'größere'")
            if 'mhelose' in bullets:
                problems.append("'mhelose' should be 'mühelose'")
            
            print(f"\n⚠️ Problems found: {len(problems)}")
            for problem in problems:
                print(f"   - {problem}")
            
            success = bullet_umlauts > 0 and len(problems) < 2
            print(f"🏆 German bullet fix: {'✅ PASS' if success else '❌ FAIL'}")
            return success
            
        else:
            print("❌ German generation failed")
            return False
            
    except Exception as e:
        print(f"❌ German test error: {e}")
        return False

def main():
    """Run both tests"""
    print("🌍 INTERNATIONAL LANGUAGE TESTING")
    print("=" * 80)
    
    polish_success = test_polish_language()
    german_success = test_german_bullet_fix()
    
    print(f"\n🏆 FINAL RESULTS:")
    print(f"   Polish support: {'✅ WORKING' if polish_success else '❌ NEEDS WORK'}")
    print(f"   German bullet fix: {'✅ FIXED' if german_success else '❌ STILL BROKEN'}")
    
    overall = "✅ SUCCESS" if (polish_success and german_success) else "⚠️ PARTIAL" if (polish_success or german_success) else "❌ FAILED"
    print(f"   Overall: {overall}")

if __name__ == "__main__":
    main()