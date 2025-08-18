#!/usr/bin/env python3
"""
TEST TURKEY MARKET LISTING GENERATION - EXACT MEXICO PATTERN IMPLEMENTATION
Testing the exact same high-quality structure applied to Turkey market
Target: 10/10 quality that beats Helium 10, Jasper AI, Copy Monkey
"""

import os
import sys
import django
import json
from datetime import datetime

# Add backend to Python path
backend_path = os.path.join(os.getcwd(), 'backend')
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.services import ListingGeneratorService
from apps.core.models import Product

def test_turkey_premium_listing():
    """Test Turkey listing generation with Mexico-level quality"""
    
    print("🇹🇷 TURKEY PREMIUM LISTING GENERATION TEST")
    print("=" * 60)
    print("📋 Testing Mexico pattern applied to Turkey market")
    print("🎯 Target: 10/10 quality exceeding all competitors")
    print()
    
    # Create test product for Turkey
    from django.contrib.auth.models import User
    user, created = User.objects.get_or_create(username='test_user')
    
    product = Product.objects.create(
        user=user,
        name="Premium Bluetooth Kulaklık Seti",
        brand_name="TechPro",
        marketplace="tr",
        marketplace_language="tr", 
        price=299.99,
        occasion="yeni_yil",  # Turkish New Year
        brand_tone="luxury",  # Premium positioning like Mexico
        categories="Electronics > Audio",
        description="Yüksek kaliteli Bluetooth kulaklık seti premium ses deneyimi için. Türk aileleri için tasarlanmış rahat kullanım.",
        features="Bluetooth 5.3 teknolojisi\n30 saat pil ömrü\nGürültü engelleme\nIPX5 su direnci\nHızlı şarj"
    )
    
    print(f"✅ Test Product Created:")
    print(f"   📦 Product: {product.name}")
    print(f"   🏪 Marketplace: {product.marketplace}")
    print(f"   🗣️ Language: {product.marketplace_language}")
    print(f"   🎉 Occasion: {product.occasion}")
    print(f"   🎨 Brand Tone: {product.brand_tone}")
    print()
    
    # Generate listing
    service = ListingGeneratorService()
    
    try:
        print("🤖 Generating Turkey listing with Mexico pattern...")
        print("⏳ Processing...")
        
        listing = service.generate_listing(product.id, 'amazon')
        
        print(f"✅ Listing Generated Successfully!")
        print(f"📊 Status: {listing.status}")
        print()
        
        # Display results
        print("🏆 TURKEY LISTING RESULTS - MEXICO PATTERN APPLIED")
        print("=" * 60)
        
        print(f"📝 TITLE ({len(listing.title)} chars):")
        print(f"   {listing.title}")
        print()
        
        print("🔸 BULLET POINTS:")
        bullet_points = listing.bullet_points.split('\n') if listing.bullet_points else []
        for i, bullet in enumerate(bullet_points, 1):
            if bullet.strip():
                print(f"   {i}. {bullet.strip()} ({len(bullet.strip())} chars)")
        print()
        
        print(f"📄 DESCRIPTION ({len(listing.long_description)} chars):")
        description_paragraphs = listing.long_description.split('\n\n')
        for i, paragraph in enumerate(description_paragraphs, 1):
            print(f"   Paragraph {i}: {paragraph.strip()}")
            print(f"   Length: {len(paragraph.strip())} chars")
            print()
        
        print(f"🔍 BACKEND KEYWORDS ({len(listing.amazon_backend_keywords)} chars):")
        print(f"   {listing.amazon_backend_keywords}")
        print()
        
        # Analyze quality metrics
        print("📊 QUALITY ANALYSIS - TURKEY vs MEXICO PATTERN")
        print("=" * 50)
        
        # Check Mexico-style formality phrases
        formality_phrases = [
            'size garanti ediyoruz',
            'size sunuyoruz', 
            'büyük bir gururla',
            'emin olabilirsiniz',
            'hiç şüphesiz'
        ]
        
        formality_count = 0
        for bullet in bullet_points:
            for phrase in formality_phrases:
                if phrase in bullet.lower():
                    formality_count += 1
                    break
        
        print(f"🎯 Turkish Formality Usage: {formality_count}/5 bullets")
        
        # Check family emphasis (Mexico pattern)
        family_words = ['aile', 'ailesi', 'aileler', 'aileye', 'ailenik']
        family_count = sum(1 for bullet in bullet_points 
                          if any(word in bullet.lower() for word in family_words))
        print(f"👨‍👩‍👧‍👦 Family Emphasis: {family_count}/{len(bullet_points)} bullets")
        
        # Check Turkish pride elements
        pride_words = ['türk', 'türkiye', 'türkiye\'de', 'türkiye\'den']
        pride_count = sum(1 for bullet in bullet_points 
                         if any(word in bullet.lower() for word in pride_words))
        print(f"🇹🇷 Turkish Pride: {pride_count}/{len(bullet_points)} bullets")
        
        # Check power words
        power_words = ['inanılmaz', 'mükemmel', 'kusursuz', 'garantili', 'premium', 'süper', 'muhteşem', 'fantastik']
        power_count = 0
        for bullet in bullet_points:
            bullet_power_count = sum(1 for word in power_words if word in bullet.lower())
            power_count += min(bullet_power_count, 3)  # Max 3 per bullet
        print(f"⚡ Power Words Usage: {power_count}/{len(bullet_points)*3} total")
        
        # A+ Content Analysis
        if listing.amazon_aplus_content:
            print(f"🎨 A+ Content Generated: {len(listing.amazon_aplus_content)} chars")
            aplus_sections = listing.amazon_aplus_content.count('<div class="aplus-section">')
            print(f"📋 A+ Sections: {aplus_sections}")
        else:
            print("❌ No A+ Content Generated")
        
        print()
        
        # Overall Quality Score
        total_score = 0
        max_score = 100
        
        # Title quality (20 points)
        title_score = min(20, len(listing.title) * 20 // 200)
        total_score += title_score
        print(f"📝 Title Quality: {title_score}/20")
        
        # Bullet formality (25 points)
        formality_score = formality_count * 5
        total_score += formality_score
        print(f"🎯 Formality Score: {formality_score}/25")
        
        # Family emphasis (15 points) 
        family_score = family_count * 3
        total_score += family_score
        print(f"👨‍👩‍👧‍👦 Family Score: {family_score}/15")
        
        # Turkish pride (15 points)
        pride_score = pride_count * 3
        total_score += pride_score
        print(f"🇹🇷 Pride Score: {pride_score}/15")
        
        # Power words (15 points)
        power_score = min(15, power_count)
        total_score += power_score
        print(f"⚡ Power Score: {power_score}/15")
        
        # A+ Content (10 points)
        aplus_score = 10 if listing.amazon_aplus_content else 0
        total_score += aplus_score
        print(f"🎨 A+ Score: {aplus_score}/10")
        
        print()
        print(f"🏆 OVERALL QUALITY SCORE: {total_score}/100")
        
        if total_score >= 90:
            print("🥇 EXCELLENT - Exceeds Helium 10/Jasper AI/Copy Monkey!")
        elif total_score >= 80:
            print("🥈 VERY GOOD - Competitive with top tools")
        elif total_score >= 70:
            print("🥉 GOOD - Above average quality")
        else:
            print("❌ NEEDS IMPROVEMENT")
            
        # Save detailed analysis
        analysis_data = {
            "timestamp": datetime.now().isoformat(),
            "product_id": product.id,
            "marketplace": "tr",
            "quality_scores": {
                "title": title_score,
                "formality": formality_score,
                "family_emphasis": family_score,
                "turkish_pride": pride_score,
                "power_words": power_score,
                "aplus_content": aplus_score,
                "total": total_score
            },
            "listing_data": {
                "title": listing.title,
                "bullets": bullet_points,
                "description": listing.long_description,
                "backend_keywords": listing.amazon_backend_keywords,
                "aplus_length": len(listing.amazon_aplus_content) if listing.amazon_aplus_content else 0
            }
        }
        
        with open(f'turkey_premium_listing_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json', 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Analysis saved to turkey_premium_listing_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
    except Exception as e:
        print(f"❌ Error generating listing: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        product.delete()
        print(f"\n🧹 Test product cleaned up")

if __name__ == "__main__":
    test_turkey_premium_listing()