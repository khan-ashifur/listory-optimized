"""
Debug what AI is actually returning in seoKeywords field
"""

import os
import sys
import django

# Add the project path and configure Django
project_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

def debug_seo_keywords():
    """Debug what AI returns in seoKeywords field"""
    
    try:
        from apps.listings.services import ListingGeneratorService
        from apps.core.models import Product
        from django.contrib.auth.models import User
        import json

        print("🔍 DEBUGGING SEO KEYWORDS FROM AI...")
        print("=" * 60)
        
        user, _ = User.objects.get_or_create(username='debug_seo', defaults={'email': 'test@debug.com'})
        
        # Create a mock result to intercept AI response
        original_generate = ListingGeneratorService._call_openai_api
        ai_response_data = {}
        
        def capture_ai_response(self, prompt):
            result = original_generate(self, prompt)
            if result:
                ai_response_data['response'] = result
            return result
            
        ListingGeneratorService._call_openai_api = capture_ai_response
        
        # Test generation
        product = Product.objects.create(
            user=user,
            name='テストイヤホン',
            description='テスト用商品',
            brand_name='TestBrand',
            marketplace='jp',
            marketplace_language='ja'
        )
        
        service = ListingGeneratorService()
        result = service.generate_listing(product.id, 'amazon')
        
        # Analyze what AI returned
        if 'response' in ai_response_data:
            ai_result = ai_response_data['response']
            
            print("🤖 AI RESPONSE ANALYSIS:")
            print("-" * 30)
            
            # Check seoKeywords structure
            seo_keywords = ai_result.get('seoKeywords', {})
            print(f"   seoKeywords found: {'✅' if seo_keywords else '❌'}")
            
            if seo_keywords:
                print(f"   seoKeywords keys: {list(seo_keywords.keys())}")
                
                for key, value in seo_keywords.items():
                    if isinstance(value, list):
                        print(f"   {key}: {len(value)} items")
                        if value:
                            print(f"     Sample: {value[0]}")
                    else:
                        print(f"   {key}: {type(value).__name__} - {str(value)[:50]}...")
                
                # Check specific categories
                primary = seo_keywords.get('primary', [])
                long_tail = seo_keywords.get('longTail', [])
                
                print(f"\n📊 KEYWORD BREAKDOWN:")
                print(f"   Primary keywords: {len(primary)}")
                print(f"   Long-tail keywords: {len(long_tail)}")
                
                if long_tail:
                    print(f"\n   Long-tail examples:")
                    for i, kw in enumerate(long_tail[:5], 1):
                        word_count = len(str(kw).split())
                        print(f"     {i}. '{kw}' ({word_count} words)")
                
            else:
                print("❌ No seoKeywords in AI response!")
                print(f"Available keys: {list(ai_result.keys())}")
        
        product.delete()
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_seo_keywords()