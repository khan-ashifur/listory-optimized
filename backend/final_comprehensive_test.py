#!/usr/bin/env python3
"""
Final comprehensive test to ensure all sections generate consistently.
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

def final_comprehensive_test():
    """Final test to ensure all sections generate consistently."""
    print("🎯 FINAL COMPREHENSIVE TEST - ALL SECTIONS")
    print("=" * 60)
    
    # Get or create user
    user, _ = User.objects.get_or_create(username='testuser', defaults={'email': 'test@example.com'})
    
    # Create comprehensive test product
    product = Product.objects.create(
        name='Ultra Premium Smart Fitness Tracker Watch Pro Max 2024',
        user=user,
        description='Advanced fitness tracking smartwatch with heart rate monitoring, GPS tracking, waterproof design, 7-day battery life, sleep analysis, and comprehensive health metrics. Perfect for athletes, fitness enthusiasts, and health-conscious individuals.',
        brand_name='FitTech',
        brand_tone='professional',
        target_platform='amazon',
        price=199.99,
        categories='Sports & Outdoors, Fitness Trackers, Smartwatches, Wearable Technology',
        features='Heart rate monitoring, GPS tracking, 7-day battery, waterproof IPX8, sleep tracking, step counter, calorie burn tracking, smartphone notifications, customizable watch faces, multiple sport modes',
        target_keywords='fitness tracker, smartwatch, heart rate monitor, GPS watch, fitness watch',
        seo_keywords='best fitness tracker 2024, waterproof smartwatch, GPS fitness watch, heart rate monitor watch',
        long_tail_keywords='fitness tracker with GPS and heart rate monitor, waterproof smartwatch for swimming, best fitness watch for runners',
        faqs='Q: Is it waterproof? A: Yes, IPX8 rated for swimming and rain. Q: How long does battery last? A: Up to 7 days with normal use. Q: Does it work with iPhone? A: Yes, compatible with iOS and Android.',
        whats_in_box='Fitness tracker watch, charging cable, user manual, warranty card, quick start guide',
        competitor_urls='https://www.amazon.com/competitor-fitness-tracker'
    )
    
    print(f"✅ Created comprehensive test product: {product.name}")
    
    # Generate listing
    generator = ListingGeneratorService()
    print("\n🚀 Generating comprehensive Amazon listing...")
    
    try:
        listing = generator.generate_listing(product.id, 'amazon')
        
        print("\n📊 COMPREHENSIVE SECTION VERIFICATION:")
        print("=" * 50)
        
        # Define all sections that should be generated
        required_sections = {
            'Core Content': [
                ('title', 'Title', 150),
                ('long_description', 'Description', 1500),
                ('bullet_points', 'Bullet Points', 750),
            ],
            'Keywords': [
                ('keywords', 'Short Tail Keywords', 100),
                ('amazon_backend_keywords', 'Backend Keywords', 200),
            ],
            'A+ Content': [
                ('amazon_aplus_content', 'A+ Content HTML', 2000),
                ('hero_title', 'Hero Title', 20),
                ('hero_content', 'Hero Content', 100),
                ('features', 'Features', 50),
                ('whats_in_box', "What's in Box", 50),
                ('trust_builders', 'Trust Builders', 50),
                ('faqs', 'FAQs', 200),
                ('social_proof', 'Social Proof', 50),
                ('guarantee', 'Guarantee', 50),
            ],
            'Quality Scores': [
                ('quality_score', 'Quality Score', None),
                ('emotion_score', 'Emotion Score', None),
                ('conversion_score', 'Conversion Score', None),
                ('trust_score', 'Trust Score', None),
            ]
        }
        
        overall_success = True
        category_results = {}
        
        for category, sections in required_sections.items():
            print(f"\n📋 {category.upper()}:")
            print("-" * 30)
            
            category_success = True
            category_details = []
            
            for field_name, display_name, min_length in sections:
                field_value = getattr(listing, field_name, None)
                
                if field_value is None:
                    status = "❌ MISSING"
                    category_success = False
                    overall_success = False
                elif field_name.endswith('_score'):
                    # Quality scores - just check if they exist
                    if field_value > 0:
                        status = f"✅ {field_value}/10"
                    else:
                        status = "❌ NOT SET"
                        category_success = False
                        overall_success = False
                else:
                    # Text fields - check length
                    content_length = len(str(field_value).strip())
                    if content_length == 0:
                        status = "❌ EMPTY"
                        category_success = False
                        overall_success = False
                    elif min_length and content_length < min_length:
                        status = f"⚠️ TOO SHORT ({content_length}/{min_length} chars)"
                        category_success = False
                        overall_success = False
                    else:
                        status = f"✅ {content_length} chars"
                
                print(f"   {display_name}: {status}")
                category_details.append((display_name, status))
            
            category_results[category] = {
                'success': category_success,
                'details': category_details
            }
        
        # Special verification for keywords
        print(f"\n🔍 DETAILED KEYWORD VERIFICATION:")
        print("-" * 40)
        
        if listing.keywords:
            keywords_list = [k.strip() for k in listing.keywords.split(',') if k.strip()]
            print(f"📌 Short Tail Keywords: {len(keywords_list)} found")
            print(f"   Examples: {', '.join(keywords_list[:3])}")
            
            if len(keywords_list) < 10:
                print(f"   ⚠️ Warning: Only {len(keywords_list)} keywords (recommend 15+)")
        
        if listing.amazon_backend_keywords:
            backend_length = len(listing.amazon_backend_keywords)
            print(f"🔧 Backend Keywords: {backend_length} characters")
            if backend_length < 200:
                print(f"   ⚠️ Warning: Only {backend_length} chars (recommend 240+)")
        
        # Check A+ Content sections specifically
        print(f"\n🎨 A+ CONTENT SECTIONS VERIFICATION:")
        print("-" * 40)
        
        if listing.amazon_aplus_content:
            content = listing.amazon_aplus_content.lower()
            aplus_sections = [
                ("Hero Section", "hero"),
                ("Features Section", "features"),
                ("Comparison Section", "comparison"),
                ("Usage Section", "usage"),
                ("Lifestyle Section", "lifestyle"),
                ("A+ Content Suggestions", "suggestions"),
                ("PPC Strategy", "ppc"),
                ("Brand Summary", "brand")
            ]
            
            missing_aplus = []
            for section_name, keyword in aplus_sections:
                if keyword in content:
                    print(f"   ✅ {section_name}")
                else:
                    print(f"   ❌ {section_name}")
                    missing_aplus.append(section_name)
            
            if missing_aplus:
                overall_success = False
                print(f"\n   🔧 Missing A+ sections: {', '.join(missing_aplus)}")
        
        # Final summary
        print(f"\n🎯 FINAL VERIFICATION SUMMARY:")
        print("=" * 50)
        
        for category, result in category_results.items():
            status_icon = "✅" if result['success'] else "❌"
            print(f"{status_icon} {category}: {'PASS' if result['success'] else 'FAIL'}")
        
        if overall_success:
            print(f"\n🎉 SUCCESS: ALL SECTIONS GENERATING CORRECTLY!")
            print(f"📊 System Status: PRODUCTION READY")
        else:
            print(f"\n⚠️ ISSUES FOUND: Some sections need attention")
            print(f"📊 System Status: NEEDS REFINEMENT")
        
        return listing, overall_success
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, False
    finally:
        # Clean up test product
        product.delete()
        print(f"\n🧹 Cleaned up test product")

if __name__ == "__main__":
    final_comprehensive_test()