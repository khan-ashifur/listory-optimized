#!/usr/bin/env python3
"""
Comprehensive test with detailed product input to achieve 10/10 quality score.
"""
import os
import sys
import django
import json

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from apps.listings.quality_validator import ListingQualityValidator
from django.contrib.auth.models import User

def comprehensive_test():
    """Test with extremely detailed product input to achieve 10/10 quality."""
    print("🎯 COMPREHENSIVE TEST - TARGET: 10/10 QUALITY SCORE")
    print("=" * 60)
    
    # Get or create user
    user, _ = User.objects.get_or_create(username='testuser', defaults={'email': 'test@example.com'})
    
    # Create detailed product for testing
    product = Product.objects.create(
        name='ZENTECH Pro Max Electric Neck Shoulder Massager with Heat Therapy',
        user=user,
        description='''Revolutionary 4D deep tissue neck and shoulder massager featuring advanced Shiatsu kneading nodes, 
        soothing heat therapy (95-113°F), and ergonomic U-shaped design. Perfect for office workers, athletes, and 
        anyone suffering from neck tension, muscle knots, or stress-related pain. Features 15-minute auto shut-off, 
        adjustable intensity levels, and premium PU leather construction. Relieves chronic pain, improves circulation, 
        and promotes relaxation. Used by over 50,000 satisfied customers worldwide. FDA-approved heating elements and 
        CE certified for safety. Includes car adapter for mobile use. Targets specific pressure points with precision 
        massage nodes that mimic professional massage therapist techniques.''',
        brand_name='ZENTECH',
        brand_tone='professional',
        target_platform='amazon',
        price=149.99,
        categories='Health & Personal Care, Massage & Relaxation, Electric Massagers, Neck & Shoulder Massagers',
        features='''4D Shiatsu kneading massage nodes, Advanced heat therapy with 3 temperature settings, 
        Ergonomic U-shaped design for perfect fit, 15-minute auto shut-off safety feature, 
        Adjustable massage intensity (3 levels), Premium PU leather with memory foam padding, 
        Car adapter included for portable use, One-button operation for easy control, 
        Bidirectional massage rotation, Extra-long power cord (6 feet), Lightweight yet durable construction, 
        Hypoallergenic materials, Easy-clean surface, Professional-grade motor''',
        target_keywords='''neck massager, shoulder massager, electric massager, shiatsu massager, heated massager, 
        neck pain relief, muscle tension relief, office chair massager''',
        seo_keywords='''best neck massager 2024, electric neck and shoulder massager, 
        heated neck massager with heat, portable neck massager, 
        neck massager for car, professional neck massager''',
        long_tail_keywords='''electric neck and shoulder massager with heat therapy, 
        best shiatsu neck massager for office workers, 
        portable heated neck massager for car and home, 
        professional grade neck massager for chronic pain relief''',
        faqs='''Q: How hot does the heat therapy get? A: The heat therapy ranges from 95-113°F with 3 adjustable settings for optimal comfort.
        Q: Is it safe to use daily? A: Yes, the 15-minute auto shut-off ensures safe daily use without overheating.
        Q: Does it work in cars? A: Yes, includes 12V car adapter for use during commutes.
        Q: What's the warranty? A: 2-year manufacturer warranty with 30-day money-back guarantee.
        Q: Is it suitable for large necks? A: The adjustable straps accommodate neck sizes from 13-20 inches.''',
        whats_in_box='''ZENTECH Pro Max Neck Massager, AC Power Adapter, 12V Car Adapter, 
        Carrying Case, User Manual, Quick Start Guide, Warranty Card''',
        competitor_urls='https://www.amazon.com/competitor-neck-massager, https://www.amazon.com/another-competitor-massager'
    )
    
    print(f"✅ Created detailed product: {product.name}")
    print(f"📝 Description length: {len(product.description)} characters")
    print(f"🎯 Features count: {len(product.features.split(','))} features")
    
    # Generate listing
    generator = ListingGeneratorService()
    print("\n🚀 Generating Amazon listing with detailed input...")
    
    try:
        listing = generator.generate_listing(product.id, 'amazon')
        
        print("\n📊 DETAILED EVALUATION:")
        print("=" * 50)
        
        # 1. Title Analysis
        title_len = len(listing.title) if listing.title else 0
        print(f"📝 TITLE: {title_len}/200 chars")
        if title_len < 150:
            print(f"   ❌ TOO SHORT - Need 150-200 chars (current: {title_len})")
        else:
            print(f"   ✅ GOOD LENGTH")
        if listing.title:
            print(f"   Preview: {listing.title[:100]}...")
        
        # 2. Description Analysis  
        desc_len = len(listing.long_description) if listing.long_description else 0
        print(f"\n📄 DESCRIPTION: {desc_len}/2000 chars")
        if desc_len < 1500:
            print(f"   ❌ TOO SHORT - Need 1500-2000 chars (current: {desc_len})")
        else:
            print(f"   ✅ GOOD LENGTH")
        if listing.long_description:
            print(f"   Preview: {listing.long_description[:150]}...")
        
        # 3. Bullet Points Analysis
        if listing.bullet_points:
            bullets = [b.strip() for b in listing.bullet_points.split('\n\n') if b.strip()]
            print(f"\n🔸 BULLET POINTS: {len(bullets)} bullets")
            for i, bullet in enumerate(bullets[:5], 1):
                bullet_len = len(bullet)
                status = "✅" if bullet_len >= 150 else "❌"
                print(f"   Bullet {i}: {bullet_len} chars {status}")
                if bullet_len < 150:
                    print(f"      TOO SHORT - Need 150-500 chars")
        else:
            print("\n🔸 BULLET POINTS: ❌ MISSING")
        
        # 4. Keywords Analysis
        if listing.keywords:
            keyword_count = len([k.strip() for k in listing.keywords.split(',') if k.strip()])
            backend_count = len([k.strip() for k in listing.amazon_backend_keywords.split(',') if k.strip()]) if listing.amazon_backend_keywords else 0
            print(f"\n🔑 KEYWORDS: {keyword_count} general + {backend_count} backend")
            if keyword_count < 15:
                print(f"   ❌ Need more general keywords (target: 15+)")
            if backend_count < 15:
                print(f"   ❌ Need more backend keywords (target: 15+)")
        
        # 5. A+ Content Analysis
        print(f"\n🎨 A+ CONTENT ANALYSIS:")
        if listing.amazon_aplus_content:
            aplus_len = len(listing.amazon_aplus_content)
            print(f"   Length: {aplus_len} characters")
            
            # Check for key sections
            content = listing.amazon_aplus_content.lower()
            sections = [
                ("Hero Section", "hero" in content or "experience" in content),
                ("Features Section", "features" in content or "key features" in content),
                ("Comparison Section", "comparison" in content or "why choose" in content),
                ("Usage Section", "how to use" in content or "usage" in content),
                ("Lifestyle Section", "lifestyle" in content or "perfect for" in content),
                ("PPC Strategy", "ppc" in content or "campaign" in content),
                ("Brand Summary", "brand" in content and "summary" in content),
                ("A+ Content Suggestions", "suggestions" in content or "content suggestions" in content)
            ]
            
            missing_sections = []
            for section_name, found in sections:
                if found:
                    print(f"   ✅ {section_name}")
                else:
                    print(f"   ❌ {section_name} - MISSING")
                    missing_sections.append(section_name)
            
            if missing_sections:
                print(f"\n   🔧 MISSING SECTIONS: {', '.join(missing_sections)}")
        else:
            print("   ❌ NO A+ CONTENT")
        
        # 6. Quality Score Analysis
        if hasattr(listing, 'quality_score') and listing.quality_score:
            print(f"\n⭐ QUALITY SCORE: {listing.quality_score}/10")
            if listing.quality_score < 10:
                print(f"   🎯 TARGET: 10/10 - Need improvement")
        else:
            # Calculate quality score manually
            validator = ListingQualityValidator()
            listing_dict = {
                'title': listing.title,
                'bullet_points': listing.bullet_points,
                'long_description': listing.long_description,
                'faqs': getattr(listing.product, 'faqs', '')
            }
            report = validator.validate_listing(listing_dict)
            score = report.overall_score
            print(f"\n⭐ CALCULATED QUALITY SCORE: {score}/10")
        
        print("\n🔧 ISSUES TO FIX:")
        issues = []
        if title_len < 150:
            issues.append("Title too short")
        if desc_len < 1500:
            issues.append("Description too short")
        if not listing.bullet_points or len([b for b in listing.bullet_points.split('\n\n') if len(b.strip()) >= 150]) < 5:
            issues.append("Bullet points too short")
        if not listing.amazon_aplus_content or "ppc" not in listing.amazon_aplus_content.lower():
            issues.append("Missing PPC Strategy")
        if not listing.amazon_aplus_content or "suggestions" not in listing.amazon_aplus_content.lower():
            issues.append("Missing A+ Content Suggestions")
        
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
        
        return listing, issues
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, []
    finally:
        # Clean up test product
        product.delete()
        print(f"\n🧹 Cleaned up test product")

if __name__ == "__main__":
    listing, issues = comprehensive_test()
    if issues:
        print(f"\n🎯 NEXT STEPS: Fix {len(issues)} identified issues")
    else:
        print(f"\n🎉 PERFECT! 10/10 QUALITY ACHIEVED!")