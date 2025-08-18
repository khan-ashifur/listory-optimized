"""
Final UAE Market Validation - Complete Field Testing
Verifies all fields are generating properly for UAE market with Arabic content
"""

import os
import sys
import json
import django

# Django setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from django.contrib.auth.models import User

def final_uae_validation():
    print("\n🇦🇪 FINAL UAE MARKET VALIDATION - ARABIC CONTENT")
    print("=" * 60)
    
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username='final_uae_test')
    
    # Test comprehensive UAE product with Eid occasion
    product = Product.objects.create(
        user=test_user,
        name="Luxury Traditional Coffee Maker",
        description="Premium Arabic coffee maker with traditional brewing method and modern convenience",
        brand_name="ArabCafe",
        brand_tone="luxurious",
        target_platform="amazon",
        marketplace="ae",
        marketplace_language="ar",  # Critical for Arabic generation
        categories="Home/Kitchen/Coffee Makers",
        features="Traditional Brewing, Premium Materials, Temperature Control, Easy Cleaning",
        target_audience="UAE families who appreciate traditional Arabic coffee culture",
        occasion="eid_al_adha"  # Eid al-Adha - Feast of Sacrifice
    )
    
    try:
        print("⏳ Generating comprehensive Arabic listing...")
        listing = service.generate_listing(product_id=product.id, platform='amazon')
        
        if listing:
            print("\n✅ FIELD VERIFICATION:")
            
            # Core fields to check
            fields_to_check = [
                ('title', listing.title),
                ('long_description', listing.long_description),
                ('bullet_points', listing.bullet_points),
                ('amazon_keywords', listing.amazon_keywords),
                ('amazon_backend_keywords', listing.amazon_backend_keywords),
                ('amazon_aplus_content', listing.amazon_aplus_content)
            ]
            
            all_fields_generated = True
            arabic_content_count = 0
            eid_content_count = 0
            
            for field_name, field_value in fields_to_check:
                if field_value and field_value.strip():
                    # Check for Arabic characters (Arabic Unicode range: U+0600 to U+06FF)
                    has_arabic = any('\u0600' <= char <= '\u06FF' for char in field_value)
                    
                    # Check for Eid-related content
                    eid_words = ['عيد', 'الأضحى', 'مبارك', 'العائلة', 'تجمع', 'ضيافة']
                    has_eid = any(word in field_value for word in eid_words)
                    
                    print(f"  • {field_name}: ✅ Generated ({len(field_value)} chars)")
                    if has_arabic:
                        print(f"    └─ 🇦🇪 Contains Arabic characters")
                        arabic_content_count += 1
                    else:
                        print(f"    └─ ⚠️  English content")
                    
                    if has_eid:
                        print(f"    └─ 🎉 Contains Eid context")
                        eid_content_count += 1
                        
                else:
                    print(f"  • {field_name}: ❌ Missing or empty")
                    all_fields_generated = False
            
            print(f"\n📊 SUMMARY:")
            print(f"  • All Fields Generated: {'✅ YES' if all_fields_generated else '❌ NO'}")
            print(f"  • Arabic Content Fields: {arabic_content_count}/6")
            print(f"  • Eid Cultural Context Fields: {eid_content_count}/6")
            print(f"  • Cultural Adaptation: {'✅ EXCELLENT' if arabic_content_count >= 4 else '⚠️ NEEDS IMPROVEMENT'}")
            
            # Save comprehensive sample
            comprehensive_sample = {
                'title': listing.title,
                'description': listing.long_description,
                'bullet_points': listing.bullet_points,
                'keywords': listing.amazon_keywords,
                'backend_keywords': listing.amazon_backend_keywords,
                'aplus_content': listing.amazon_aplus_content[:500] if listing.amazon_aplus_content else None,
                'validation': {
                    'all_fields_generated': all_fields_generated,
                    'arabic_content_fields': arabic_content_count,
                    'eid_content_fields': eid_content_count,
                    'total_fields': len(fields_to_check)
                }
            }
            
            with open('final_uae_validation.json', 'w', encoding='utf-8') as f:
                json.dump(comprehensive_sample, f, indent=2, ensure_ascii=False)
            
            print(f"\n🇦🇪 UAE MARKET STATUS:")
            if all_fields_generated and arabic_content_count >= 4:
                print("✅ READY FOR PRODUCTION")
                print("   UAE market fully implemented with Arabic cultural intelligence")
                print("   🎉 Including Eid al-Adha cultural context")
            else:
                print("⚠️ NEEDS OPTIMIZATION")
                print("   Some fields missing or lacking Arabic content")
                
        else:
            print("❌ No listing generated")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        product.delete()

if __name__ == "__main__":
    final_uae_validation()