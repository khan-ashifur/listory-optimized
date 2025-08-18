"""
Final Japan Market Validation - Complete Field Testing
Verifies all fields are generating properly for Japan market
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

def final_japan_validation():
    print("\n🇯🇵 FINAL JAPAN MARKET VALIDATION")
    print("=" * 50)
    
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username='final_japan_test')
    
    # Test comprehensive Japanese product
    product = Product.objects.create(
        user=test_user,
        name="Premium Smart Rice Cooker",
        description="Advanced AI-powered rice cooker with Japanese precision technology",
        brand_name="TechKitchen",
        brand_tone="trustworthy",
        target_platform="amazon",
        marketplace="jp",
        marketplace_language="ja",  # Critical for Japanese generation
        categories="Home/Kitchen/Small Appliances",
        features="AI Technology, 10 Cup Capacity, Multiple Cooking Modes, Keep Warm Function",
        target_audience="Japanese families and cooking enthusiasts",
        occasion="oseibo"  # End-year gift giving season
    )
    
    try:
        print("⏳ Generating comprehensive Japanese listing...")
        listing = service.generate_listing(product_id=product.id, platform='amazon')
        
        if listing:
            print("\n✅ FIELD VERIFICATION:")
            
            # Core fields
            fields_to_check = [
                ('title', listing.title),
                ('long_description', listing.long_description),
                ('bullet_points', listing.bullet_points),
                ('amazon_keywords', listing.amazon_keywords),
                ('amazon_backend_keywords', listing.amazon_backend_keywords),
                ('amazon_aplus_content', listing.amazon_aplus_content)
            ]
            
            all_fields_generated = True
            japanese_content_count = 0
            
            for field_name, field_value in fields_to_check:
                if field_value and field_value.strip():
                    # Check for Japanese characters
                    has_japanese = any('\u3040' <= char <= '\u309F' or '\u30A0' <= char <= '\u30FF' or '\u4E00' <= char <= '\u9FFF' for char in field_value)
                    
                    print(f"  • {field_name}: ✅ Generated ({len(field_value)} chars)")
                    if has_japanese:
                        print(f"    └─ 🇯🇵 Contains Japanese characters")
                        japanese_content_count += 1
                    else:
                        print(f"    └─ ⚠️  English content")
                else:
                    print(f"  • {field_name}: ❌ Missing or empty")
                    all_fields_generated = False
            
            print(f"\n📊 SUMMARY:")
            print(f"  • All Fields Generated: {'✅ YES' if all_fields_generated else '❌ NO'}")
            print(f"  • Japanese Content Fields: {japanese_content_count}/6")
            print(f"  • Cultural Adaptation: {'✅ EXCELLENT' if japanese_content_count >= 4 else '⚠️ NEEDS IMPROVEMENT'}")
            
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
                    'japanese_content_fields': japanese_content_count,
                    'total_fields': len(fields_to_check)
                }
            }
            
            with open('final_japan_validation.json', 'w', encoding='utf-8') as f:
                json.dump(comprehensive_sample, f, indent=2, ensure_ascii=False)
            
            print(f"\n🎌 JAPAN MARKET STATUS:")
            if all_fields_generated and japanese_content_count >= 4:
                print("✅ READY FOR PRODUCTION")
                print("   Japan market fully implemented with cultural intelligence")
            else:
                print("⚠️ NEEDS OPTIMIZATION")
                print("   Some fields missing or lacking Japanese content")
                
        else:
            print("❌ No listing generated")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        product.delete()

if __name__ == "__main__":
    final_japan_validation()