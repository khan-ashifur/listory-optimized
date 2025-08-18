"""
Test final Japanese keywords generation with amazon_keywords field
"""

import os
import sys
import django

# Add the project path and configure Django
project_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

def test_japanese_keywords_final():
    """Test final Japanese keyword generation"""
    
    try:
        from apps.listings.services import ListingGeneratorService
        from apps.core.models import Product
        from django.contrib.auth.models import User

        print("🇯🇵 TESTING FINAL JAPANESE KEYWORDS...")
        print("=" * 50)
        
        user, _ = User.objects.get_or_create(username='jp_final_test', defaults={'email': 'test@amazon.co.jp'})
        product = Product.objects.create(
            user=user,
            name='プレミアムワイヤレスイヤホン',
            description='高品質ノイズキャンセリング機能',
            brand_name='TechSound',
            brand_tone='professional',
            target_platform='amazon',
            marketplace='jp',
            marketplace_language='ja',
            price=12800,
            categories='Electronics,Audio',
            features='ノイズキャンセリング,30時間バッテリー'
        )
        
        service = ListingGeneratorService()
        result = service.generate_listing(product.id, 'amazon')
        
        if result:
            keywords = getattr(result, 'keywords', '')
            amazon_keywords = getattr(result, 'amazon_keywords', '')
            backend_keywords = getattr(result, 'amazon_backend_keywords', '')
            
            if keywords:
                keyword_list = [k.strip() for k in keywords.split(',') if k.strip()]
                short_tail = [k for k in keyword_list if len(k.split()) <= 2]
                long_tail = [k for k in keyword_list if len(k.split()) > 2]
                
                print(f"📊 JAPANESE KEYWORD RESULTS:")
                print(f"   🎌 Total keywords: {len(keyword_list)}")
                print(f"   📈 Short-tail: {len(short_tail)} keywords")
                print(f"   📈 Long-tail: {len(long_tail)} keywords")
                print(f"   🔄 Backend: {len(backend_keywords)} chars")
                print(f"   🎯 amazon_keywords field: {'✅ POPULATED' if amazon_keywords else '❌ EMPTY'}")
                print(f"   🔗 Fields match: {'✅' if keywords == amazon_keywords else '❌'}")
                
                # Check if comprehensive (75+ expected)
                is_comprehensive = len(keyword_list) >= 75
                print(f"   🏆 Comprehensive: {'✅ EXCELLENT' if is_comprehensive else '❌ NEEDS MORE'} ({len(keyword_list)}/75+ expected)")
                
                # Show samples
                japanese_keywords = [k for k in keyword_list[:10] if any('\u3040' <= char <= '\u309f' or '\u30a0' <= char <= '\u30ff' or '\u4e00' <= char <= '\u9faf' for char in k)]
                print(f"   🗾 Japanese samples: {', '.join(japanese_keywords[:3])}...")
                
                if is_comprehensive:
                    print(f"\n🎉 SUCCESS: Japanese keywords now show {len(keyword_list)} total instead of '1 Short-tail 1 Long-tail 1 Backend Terms only'!")
                    return True
                else:
                    print(f"\n⚠️ Still needs work: Only {len(keyword_list)} keywords generated")
                    return False
            else:
                print("❌ No keywords generated")
                return False
        else:
            print("❌ Failed to generate listing")
            return False
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        try:
            product.delete()
        except:
            pass

if __name__ == "__main__":
    success = test_japanese_keywords_final()
    print(f"\n{'🎌 JAPANESE KEYWORDS WORKING!' if success else '🔧 STILL NEEDS WORK'}")