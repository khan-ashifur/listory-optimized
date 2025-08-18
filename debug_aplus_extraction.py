"""
Debug A+ content extraction for Japanese market
"""

import os
import sys
import django

# Add the project path and configure Django
project_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

def debug_aplus_extraction():
    """Debug A+ content extraction"""
    
    try:
        from apps.listings.services import ListingGeneratorService
        from apps.core.models import Product
        from django.contrib.auth.models import User

        print("🔍 DEBUGGING A+ CONTENT EXTRACTION...")
        print("=" * 50)
        
        user, _ = User.objects.get_or_create(username='debug_aplus', defaults={'email': 'test@test.com'})
        product = Product.objects.create(
            user=user,
            name='テストイヤホン',
            description='高品質テスト',
            brand_name='TestBrand',
            marketplace='jp',
            marketplace_language='ja'
        )
        
        # Intercept the extraction process
        service = ListingGeneratorService()
        
        # Override the A+ content assignment to debug
        original_generate = service._generate_amazon_listing
        
        def debug_generate(product, listing):
            result = original_generate(product, listing)
            
            print(f"📋 DEBUG A+ CONTENT EXTRACTION:")
            print(f"   A+ content length: {len(getattr(listing, 'amazon_aplus_content', ''))} chars")
            print(f"   A+ content sample: {getattr(listing, 'amazon_aplus_content', '')[:200]}...")
            
            # Check for Japanese characters in A+ content
            aplus_content = getattr(listing, 'amazon_aplus_content', '')
            has_japanese = any('\u3040' <= c <= '\u309f' or '\u30a0' <= c <= '\u30ff' or '\u4e00' <= c <= '\u9faf' for c in aplus_content)
            print(f"   Has Japanese characters: {'✅' if has_japanese else '❌'}")
            
            return result
        
        service._generate_amazon_listing = debug_generate
        
        result = service.generate_listing(product.id, 'amazon')
        
        if result:
            print("✅ Listing generated successfully!")
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
    debug_aplus_extraction()