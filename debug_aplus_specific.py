"""
Debug specific A+ content issue for Japanese
"""

import os
import sys
import django

# Add the project path and configure Django
project_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

def debug_aplus_specific():
    """Debug specific A+ content generation"""
    
    try:
        from apps.listings.services import ListingGeneratorService
        from apps.core.models import Product
        from django.contrib.auth.models import User

        print("🔍 DEBUGGING JAPANESE A+ CONTENT SPECIFIC ISSUE...")
        print("=" * 60)
        
        user, _ = User.objects.get_or_create(username='debug_aplus_jp', defaults={'email': 'test@test.com'})
        product = Product.objects.create(
            user=user,
            name='テストイヤホン',
            description='高品質テスト',
            brand_name='TestBrand',
            marketplace='jp',
            marketplace_language='ja'
        )
        
        service = ListingGeneratorService()
        result = service.generate_listing(product.id, 'amazon')
        
        if result:
            aplus_content = getattr(result, 'amazon_aplus_content', '')
            
            print(f"📄 A+ CONTENT ANALYSIS:")
            print(f"   Length: {len(aplus_content)} characters")
            print(f"   Sample (first 500 chars):")
            print(f"   {aplus_content[:500]}")
            print(f"   ...")
            print(f"   Last 200 chars:")
            print(f"   ...{aplus_content[-200:]}")
            
            # Check content composition
            has_japanese = any('\u3040' <= c <= '\u309f' or '\u30a0' <= c <= '\u30ff' or '\u4e00' <= c <= '\u9faf' for c in aplus_content)
            has_english_html = any(word in aplus_content for word in ['<div class=', 'bg-gradient', 'text-purple', 'aplus-introduction'])
            has_clean_html = '<h3>' in aplus_content and '</h3>' in aplus_content
            
            print(f"\n   Content Analysis:")
            print(f"   ✅ Contains Japanese: {has_japanese}")
            print(f"   ❌ Contains English HTML classes: {has_english_html}")  
            print(f"   ✅ Has clean HTML structure: {has_clean_html}")
            
            if has_english_html:
                print(f"\n   🚨 PROBLEM: A+ content contains English HTML structure!")
                print(f"   This means the localization fix isn't working properly.")
            elif has_japanese and has_clean_html:
                print(f"\n   🎉 SUCCESS: A+ content is properly localized!")
            
        else:
            print("❌ Failed to generate listing")
        
        product.delete()
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_aplus_specific()