#!/usr/bin/env python3
"""
TEST TURKEY A+ CONTENT FIX
Verify that Turkey now uses AI-generated Turkish content instead of generic template
"""

import os
import sys
import django
from datetime import datetime

# Add backend to Python path
backend_path = os.path.join(os.getcwd(), 'backend')
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.services import ListingGeneratorService
from apps.core.models import Product

def test_turkey_aplus_fix():
    """Test that Turkey A+ content fix works properly"""
    
    print("🇹🇷 TESTING TURKEY A+ CONTENT FIX")
    print("=" * 40)
    
    from django.contrib.auth.models import User
    user, created = User.objects.get_or_create(username='test_aplus_fix')
    
    # Create Turkey product
    product = Product.objects.create(
        user=user,
        name="Premium Kulaklık Test",
        brand_name="TestBrand",
        marketplace="tr",
        marketplace_language="tr", 
        price=299.99,
        occasion="yeni_yil",
        brand_tone="luxury",
        categories="Electronics > Audio",
        description="Premium Turkish headphones test",
        features="Bluetooth 5.3\n30 saat pil\nGürültü engelleme"
    )
    
    print(f"✅ Test Product Created: {product.name}")
    print(f"📍 Marketplace: {product.marketplace}")
    
    try:
        service = ListingGeneratorService()
        listing = service.generate_listing(product.id, 'amazon')
        
        print(f"\n📊 Generation Results:")
        print(f"   Status: {listing.status}")
        print(f"   A+ Content Length: {len(listing.amazon_aplus_content):,} characters")
        
        # Analyze A+ content structure
        aplus_content = listing.amazon_aplus_content
        
        # Check for improvements
        print(f"\n🔍 A+ CONTENT ANALYSIS:")
        
        # Check for localized sections
        localized_sections = aplus_content.count('<div class="aplus-localized-content">')
        print(f"   ✅ Localized content sections: {localized_sections}")
        
        # Check for AI-generated sections
        ai_sections = aplus_content.count('<div class="aplus-section ')
        print(f"   ✅ AI-generated sections: {ai_sections}")
        
        # Check for Turkish content
        turkish_indicators = ['türk', 'aile', 'kalite', 'garanti', 'ürün', 'müşteri']
        turkish_found = sum(1 for word in turkish_indicators if word in aplus_content.lower())
        print(f"   🇹🇷 Turkish content indicators: {turkish_found}/{len(turkish_indicators)}")
        
        # Check for generic English indicators
        generic_indicators = [
            'Complete A+ Content Strategy',
            'AI-Generated Briefs', 
            'Design Guidelines',
            'Ready for Production'
        ]
        generic_found = sum(1 for phrase in generic_indicators if phrase in aplus_content)
        print(f"   ❌ Generic English elements: {generic_found}/{len(generic_indicators)}")
        
        # Check structure improvements
        if localized_sections > 0:
            print(f"   ✅ IMPROVEMENT: Localized sections now included!")
        
        if ai_sections > 0:
            print(f"   ✅ IMPROVEMENT: AI-generated sections found!")
        
        # Look for specific Turkish section titles
        import re
        turkish_titles = re.findall(r'<h2 class="section-title">([^<]*(?:türk|aile|kalite|özellik|garanti)[^<]*)</h2>', aplus_content, re.IGNORECASE)
        if turkish_titles:
            print(f"   🇹🇷 Turkish section titles found: {len(turkish_titles)}")
            for title in turkish_titles[:3]:
                print(f"      • {title}")
        
        # Save the fixed A+ content
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f'turkey_aplus_fixed_{timestamp}.html', 'w', encoding='utf-8') as f:
            f.write(aplus_content)
        
        print(f"\n💾 Fixed A+ content saved to turkey_aplus_fixed_{timestamp}.html")
        
        # Assessment
        print(f"\n🎯 FIX ASSESSMENT:")
        
        improvement_score = 0
        
        if localized_sections > 0:
            improvement_score += 30
            print("   ✅ +30 points: Localized content sections added")
        
        if ai_sections > 0:
            improvement_score += 25
            print("   ✅ +25 points: AI-generated sections included")
        
        if turkish_found >= 4:
            improvement_score += 20
            print("   ✅ +20 points: Strong Turkish localization")
        elif turkish_found >= 2:
            improvement_score += 10
            print("   ✅ +10 points: Partial Turkish localization")
        
        if generic_found <= 2:
            improvement_score += 15
            print("   ✅ +15 points: Reduced generic English content")
        
        if len(aplus_content) > 25000:
            improvement_score += 10
            print("   ✅ +10 points: Comprehensive content length")
        
        print(f"\n🏆 IMPROVEMENT SCORE: {improvement_score}/100")
        
        if improvement_score >= 80:
            print("🎉 EXCELLENT FIX! Turkey A+ content now properly localized!")
        elif improvement_score >= 60:
            print("✅ GOOD FIX! Significant improvement in localization!")
        elif improvement_score >= 40:
            print("⚠️ PARTIAL FIX! Some improvements but needs more work!")
        else:
            print("❌ FIX FAILED! No significant improvement detected!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        product.delete()
        print(f"\n🧹 Test product cleaned up")

if __name__ == "__main__":
    test_turkey_aplus_fix()