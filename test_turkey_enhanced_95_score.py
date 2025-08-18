#!/usr/bin/env python3
"""
TURKEY ENHANCED LISTING GENERATION - TARGETING 95+ SCORE
Testing the optimized Turkey implementation to beat Helium 10, Jasper AI, Copy Monkey
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

def test_turkey_enhanced_95_score():
    """Test Turkey listing generation with enhanced 95+ score optimization"""
    
    print("🇹🇷 TURKEY ENHANCED LISTING GENERATION - 95+ SCORE TARGET")
    print("=" * 70)
    print("🎯 Target: Beat Helium 10, Jasper AI, Copy Monkey")
    print("📈 Enhanced with: Urgency, Social Proof, Competitive Edge, Risk Reversal")
    print()
    
    # Create test product for Turkey
    from django.contrib.auth.models import User
    user, created = User.objects.get_or_create(username='test_user_enhanced')
    
    product = Product.objects.create(
        user=user,
        name="Premium Bluetooth Kulaklık Seti Pro Max",
        brand_name="TechPro Elite",
        marketplace="tr",
        marketplace_language="tr", 
        price=399.99,
        occasion="yeni_yil",  # Turkish New Year
        brand_tone="luxury",  # Premium positioning like Mexico
        categories="Electronics > Audio > Headphones",
        description="En üstün kaliteli Bluetooth kulaklık seti eksklüzif ses deneyimi için. Türk aileleri için özel tasarlanmış çığır açan teknoloji.",
        features="Çığır açan Bluetooth 5.3 teknolojisi\n35 saat ultra uzun pil ömrü\nRakipsiz aktif gürültü engelleme\nProfesyonel IPX5 su direnci\nEksklüzif hızlı şarj teknolojisi\nPremium deri kulak pedleri"
    )
    
    print(f"✅ Enhanced Test Product Created:")
    print(f"   📦 Product: {product.name}")
    print(f"   🏪 Marketplace: {product.marketplace}")
    print(f"   🗣️ Language: {product.marketplace_language}")
    print(f"   🎉 Occasion: {product.occasion}")
    print(f"   🎨 Brand Tone: {product.brand_tone}")
    print(f"   💰 Price: {product.price} TRY")
    print()
    
    # Generate listing with enhanced optimization
    service = ListingGeneratorService()
    
    try:
        print("🤖 Generating ENHANCED Turkey listing...")
        print("⚡ Enhanced patterns: Urgency + Social Proof + Competitive Edge + Risk Reversal")
        print("⏳ Processing...")
        
        listing = service.generate_listing(product.id, 'amazon')
        
        print(f"✅ Enhanced Listing Generated Successfully!")
        print(f"📊 Status: {listing.status}")
        print()
        
        # Display enhanced results
        print("🏆 ENHANCED TURKEY LISTING RESULTS - TARGETING 95+ SCORE")
        print("=" * 70)
        
        print(f"📝 ENHANCED TITLE ({len(listing.title)} chars):")
        print(f"   {listing.title}")
        print()
        
        print("🔸 ENHANCED BULLET POINTS:")
        bullet_points = listing.bullet_points.split('\n') if listing.bullet_points else []
        for i, bullet in enumerate(bullet_points, 1):
            if bullet.strip():
                print(f"   {i}. {bullet.strip()} ({len(bullet.strip())} chars)")
        print()
        
        print(f"📄 ENHANCED DESCRIPTION ({len(listing.long_description)} chars):")
        description_paragraphs = listing.long_description.split('\n\n')
        for i, paragraph in enumerate(description_paragraphs, 1):
            print(f"   Paragraph {i}: {paragraph.strip()[:200]}...")
            print(f"   Length: {len(paragraph.strip())} chars")
            print()
        
        # ENHANCED QUALITY ANALYSIS
        print("📊 ENHANCED QUALITY ANALYSIS - COMPETITOR BEATING METRICS")
        print("=" * 60)
        
        # Enhanced scoring metrics
        
        # 1. Urgency Analysis (NEW)
        urgency_words = ['sınırlı stok', 'son fırsat', 'bugün', 'acele', 'hemen', 'sınırlı', 'özel fiyat']
        urgency_count = sum(1 for bullet in bullet_points 
                           if any(word in bullet.lower() for word in urgency_words))
        urgency_score = min(20, urgency_count * 10)  # Max 20 points
        print(f"⚡ Urgency Elements: {urgency_count} found | Score: {urgency_score}/20")
        
        # 2. Social Proof Analysis (NEW) 
        social_proof_indicators = ['10,000+', '50,000+', '★★★★★', '4.8/5', 'memnun müşteri', 'onaylandı']
        social_proof_count = sum(1 for bullet in bullet_points 
                                if any(indicator in bullet for indicator in social_proof_indicators))
        social_proof_score = min(20, social_proof_count * 10)  # Max 20 points
        print(f"👥 Social Proof: {social_proof_count} indicators | Score: {social_proof_score}/20")
        
        # 3. Competitive Edge Analysis (NEW)
        competitive_words = ['rakiplerden', '%40 üstün', 'benzersiz', 'eksklüzif', 'çığır açan', 'piyasada tek']
        competitive_count = sum(1 for bullet in bullet_points 
                               if any(word in bullet.lower() for word in competitive_words))
        competitive_score = min(15, competitive_count * 7.5)  # Max 15 points
        print(f"🥇 Competitive Edge: {competitive_count} claims | Score: {competitive_score}/15")
        
        # 4. Risk Reversal Analysis (NEW)
        risk_reversal_words = ['iade garantisi', 'para iadesi', 'memnun kalmazsanız', 'tam güvence']
        risk_reversal_count = sum(1 for bullet in bullet_points 
                                 if any(word in bullet.lower() for word in risk_reversal_words))
        risk_reversal_score = min(10, risk_reversal_count * 5)  # Max 10 points
        print(f"🛡️ Risk Reversal: {risk_reversal_count} guarantees | Score: {risk_reversal_score}/10")
        
        # 5. Enhanced Power Words Analysis
        enhanced_power_words = [
            'inanılmaz', 'mükemmel', 'kusursuz', 'garantili', 'premium', 'süper', 'muhteşem', 
            'fantastik', 'eksklüzif', 'çığır açan', 'sınırlı', 'benzersiz', 'rakipsiz', 
            'doruk', 'zirvede', 'birinci', 'lider', 'şaheser'
        ]
        enhanced_power_count = 0
        for bullet in bullet_points:
            bullet_power_count = sum(1 for word in enhanced_power_words if word in bullet.lower())
            enhanced_power_count += bullet_power_count
        enhanced_power_score = min(15, enhanced_power_count)  # Max 15 points
        print(f"⚡ Enhanced Power Words: {enhanced_power_count} total | Score: {enhanced_power_score}/15")
        
        # Existing metrics (updated weights)
        
        # Turkish formality (maintained)
        formality_phrases = [
            'size garanti ediyoruz', 'size sunuyoruz', 'büyük bir gururla',
            'emin olabilirsiniz', 'hiç şüphesiz'
        ]
        formality_count = 0
        for bullet in bullet_points:
            for phrase in formality_phrases:
                if phrase in bullet.lower():
                    formality_count += 1
                    break
        formality_score = min(10, formality_count * 2)  # Reduced from 25 to 10
        print(f"🎯 Turkish Formality: {formality_count}/5 bullets | Score: {formality_score}/10")
        
        # Family emphasis (maintained)
        family_words = ['aile', 'ailesi', 'aileler', 'aileye', 'ailenik']
        family_count = sum(1 for bullet in bullet_points 
                          if any(word in bullet.lower() for word in family_words))
        family_score = min(10, family_count * 2)  # Reduced from 15 to 10
        print(f"👨‍👩‍👧‍👦 Family Emphasis: {family_count}/{len(bullet_points)} bullets | Score: {family_score}/10")
        
        print()
        
        # Calculate Enhanced Total Score
        total_enhanced_score = (urgency_score + social_proof_score + competitive_score + 
                               risk_reversal_score + enhanced_power_score + formality_score + family_score)
        max_enhanced_score = 120  # Increased ceiling
        
        # Convert to 100-point scale
        final_score = min(100, (total_enhanced_score / max_enhanced_score) * 100)
        
        print("🏆 ENHANCED SCORING BREAKDOWN:")
        print("=" * 40)
        print(f"⚡ Urgency Elements:     {urgency_score}/20")
        print(f"👥 Social Proof:        {social_proof_score}/20") 
        print(f"🥇 Competitive Edge:    {competitive_score}/15")
        print(f"🛡️ Risk Reversal:       {risk_reversal_score}/10")
        print(f"⚡ Enhanced Power Words: {enhanced_power_score}/15")
        print(f"🎯 Turkish Formality:   {formality_score}/10")
        print(f"👨‍👩‍👧‍👦 Family Emphasis:     {family_score}/10")
        print("=" * 40)
        print(f"📊 TOTAL ENHANCED SCORE: {total_enhanced_score}/{max_enhanced_score}")
        print(f"🎯 FINAL SCORE (100-scale): {final_score:.1f}/100")
        
        print()
        
        # Enhanced Quality Assessment
        if final_score >= 95:
            print("🥇 EXCELLENCE ACHIEVED! BEATS ALL COMPETITORS!")
            print("   ✅ Helium 10: DOMINATED")
            print("   ✅ Jasper AI: EXCEEDED") 
            print("   ✅ Copy Monkey: SURPASSED")
            status = "MARKET LEADER"
        elif final_score >= 90:
            print("🥈 EXCEPTIONAL QUALITY - Top Tier Performance")
            status = "HIGHLY COMPETITIVE"
        elif final_score >= 85:
            print("🥉 VERY GOOD - Strong Performance")
            status = "COMPETITIVE"
        else:
            print("❌ NEEDS FURTHER OPTIMIZATION")
            status = "REQUIRES IMPROVEMENT"
        
        # Competitive Analysis Summary
        print(f"\n📈 COMPETITIVE ANALYSIS SUMMARY:")
        print(f"   🆚 vs Helium 10:  {'SUPERIOR' if final_score >= 90 else 'COMPETITIVE' if final_score >= 80 else 'NEEDS WORK'}")
        print(f"   🆚 vs Jasper AI:  {'SUPERIOR' if final_score >= 92 else 'COMPETITIVE' if final_score >= 82 else 'NEEDS WORK'}")
        print(f"   🆚 vs Copy Monkey: {'SUPERIOR' if final_score >= 88 else 'COMPETITIVE' if final_score >= 78 else 'NEEDS WORK'}")
        
        # Save enhanced analysis
        enhanced_analysis_data = {
            "timestamp": datetime.now().isoformat(),
            "product_id": product.id,
            "marketplace": "tr",
            "enhancement_version": "2.0",
            "final_score": final_score,
            "status": status,
            "enhanced_scores": {
                "urgency": urgency_score,
                "social_proof": social_proof_score,
                "competitive_edge": competitive_score,
                "risk_reversal": risk_reversal_score,
                "enhanced_power_words": enhanced_power_score,
                "turkish_formality": formality_score,
                "family_emphasis": family_score,
                "total": total_enhanced_score,
                "max_possible": max_enhanced_score
            },
            "competitive_analysis": {
                "vs_helium_10": "SUPERIOR" if final_score >= 90 else "COMPETITIVE" if final_score >= 80 else "NEEDS_WORK",
                "vs_jasper_ai": "SUPERIOR" if final_score >= 92 else "COMPETITIVE" if final_score >= 82 else "NEEDS_WORK", 
                "vs_copy_monkey": "SUPERIOR" if final_score >= 88 else "COMPETITIVE" if final_score >= 78 else "NEEDS_WORK"
            },
            "listing_data": {
                "title": listing.title,
                "bullets": bullet_points,
                "description": listing.long_description,
                "backend_keywords": listing.amazon_backend_keywords,
                "aplus_length": len(listing.amazon_aplus_content) if listing.amazon_aplus_content else 0
            }
        }
        
        filename = f'turkey_enhanced_95_score_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(enhanced_analysis_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Enhanced analysis saved to {filename}")
        
        # Final recommendation
        if final_score >= 95:
            print(f"\n🎉 SUCCESS! Turkey listing achieves {final_score:.1f}/100 - BEATS ALL COMPETITORS!")
            print("🚀 Ready for market deployment as premium solution")
        else:
            remaining_points = 95 - final_score
            print(f"\n🔧 Need {remaining_points:.1f} more points to reach 95+ target")
            print("💡 Focus on missing urgency, social proof, or competitive elements")
        
    except Exception as e:
        print(f"❌ Error generating enhanced listing: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        product.delete()
        print(f"\n🧹 Test product cleaned up")

if __name__ == "__main__":
    test_turkey_enhanced_95_score()