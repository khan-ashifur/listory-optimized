"""
Debug A+ content prompt response to see why aPlusContentPlan is empty
"""

import os
import sys
import django

# Add the project path and configure Django
project_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

def debug_aplus_prompt_response():
    """Debug why aPlusContentPlan is coming back empty"""
    
    try:
        from apps.listings.services import ListingGeneratorService
        from apps.core.models import Product
        from django.contrib.auth.models import User
        import json

        print("🔍 DEBUGGING A+ CONTENT PROMPT RESPONSE")
        print("=" * 50)
        
        user, _ = User.objects.get_or_create(
            username='debug_aplus_prompt', 
            defaults={'email': 'test@test.com'}
        )
        
        product = Product.objects.create(
            user=user,
            name='テストイヤホン',
            description='高品質テスト',
            brand_name='TestBrand',
            marketplace='jp',
            marketplace_language='ja',
            features='ノイズキャンセリング,バッテリー',
            price=12800
        )
        
        service = ListingGeneratorService()
        
        # Hook into the OpenAI call to capture the full response
        original_call_openai = service._call_openai_api
        
        def debug_call_openai(*args, **kwargs):
            print("📤 Making OpenAI API call...")
            result = original_call_openai(*args, **kwargs)
            
            print(f"📥 OpenAI Response length: {len(result) if result else 0} characters")
            
            if result and len(result) > 0:
                # Try to find aPlusContentPlan in the raw response
                if '"aPlusContentPlan"' in result:
                    print("✅ Found aPlusContentPlan in raw response")
                    
                    # Extract just the aPlusContentPlan section
                    import re
                    aplus_match = re.search(r'"aPlusContentPlan":\s*({.*?})\s*[,}]', result, re.DOTALL)
                    if aplus_match:
                        aplus_raw = aplus_match.group(1)
                        print(f"📋 Raw aPlusContentPlan section ({len(aplus_raw)} chars):")
                        print(aplus_raw[:500] + "..." if len(aplus_raw) > 500 else aplus_raw)
                    else:
                        print("❌ Could not extract aPlusContentPlan section")
                else:
                    print("❌ No aPlusContentPlan found in raw response")
                    print(f"📋 Response preview: {result[:1000]}...")
            
            return result
        
        service._call_openai_api = debug_call_openai
        
        # Generate listing
        result = service.generate_listing(product.id, 'amazon')
        
        if result:
            print(f"\\n📊 FINAL RESULT ANALYSIS:")
            
            # Check if we have aPlusContentPlan in the parsed result
            if hasattr(result, 'amazon_aplus_content'):
                aplus_content = getattr(result, 'amazon_aplus_content', '')
                print(f"   A+ content length: {len(aplus_content)} chars")
                
                # Check if it contains Japanese
                has_japanese = any('\\u3040' <= c <= '\\u309f' or '\\u30a0' <= c <= '\\u30ff' or '\\u4e00' <= c <= '\\u9faf' for c in aplus_content)
                print(f"   Contains Japanese: {'✅' if has_japanese else '❌'}")
                
                # Check if it's HTML or localized content
                has_html_tags = '<div class=' in aplus_content
                print(f"   Contains HTML structure: {'✅ (English fallback)' if has_html_tags else '❌ (Localized content)'}")
                
                # Show first few lines
                lines = aplus_content.split('\\n')[:5]
                print(f"   Content preview:")
                for i, line in enumerate(lines):
                    print(f"      {i+1}: {line[:80]}...")
            
            print("✅ Debug completed")
            return True
        else:
            print("❌ Failed to generate listing")
            return False
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Cleanup
        try:
            product.delete()
        except:
            pass

if __name__ == "__main__":
    debug_aplus_prompt_response()