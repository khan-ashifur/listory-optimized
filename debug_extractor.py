"""
Debug the InternationalContentExtractor directly with Japanese content
"""

import os
import sys
import django

# Add the project path and configure Django
project_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

def debug_extractor():
    """Debug the content extractor with sample Japanese content"""
    
    print("🔍 DEBUGGING INTERNATIONAL CONTENT EXTRACTOR")
    print("=" * 60)
    
    # Sample AI response that was generated (from the log above)
    sample_ai_response = """{
  "productTitle": "GW旅行用 KitchenPro プレミアム竹製まな板セット 高品質抗菌加工 日本品質 精密設計 大小2枚組 送料無料 翌日配送対応",
  "bulletPoints": [
    "🌿 GW旅行に最適: 高品質な竹材100%を使用し、日本品質の丁寧な作りで耐久性抜群です。抗菌加工により衛生的にお使いいただけます。アウトドアでの調理や家族キャンプに最適です。",
    "🍽️ 連休の外出に: 大小2枚セットで用途に合わせて使い分け可能です。40x30cmの大サイズは肉や魚、小サイズは果物やパンに便利。家庭から旅行先まで活躍いたします。",
    "🎋 ゴールデンウィークに: 滑り止め付きで安全な調理作業をサポートします。食洗機対応で連休中の手入れも簡単です。軽量で持ち運びやすく旅行先でも重宝します。"
  ],
  "productDescription": "高品質な竹製まな板セットです。抗菌加工により衛生的で、大小2枚組で用途別に使い分けができます。ゴールデンウィークの旅行や家族時間にぴったりの商品です。"
}"""
    
    try:
        from apps.listings.international_content_extractor import InternationalContentExtractor
        
        extractor = InternationalContentExtractor()
        
        print("📝 Sample AI Response (first 200 chars):")
        print(sample_ai_response[:200] + "...")
        
        # Test individual extraction methods
        print(f"\n🔍 TESTING INDIVIDUAL EXTRACTION METHODS:")
        
        # Test title extraction
        title = extractor._extract_title(sample_ai_response)
        print(f"Title extracted: '{title}' (length: {len(title)})")
        
        # Test bullets extraction  
        bullets = extractor._extract_bullets(sample_ai_response)
        print(f"Bullets extracted: {len(bullets)} items")
        for i, bullet in enumerate(bullets[:2], 1):
            print(f"  {i}. {bullet[:60]}...")
        
        # Test description extraction
        description = extractor._extract_description(sample_ai_response)
        print(f"Description extracted: '{description}' (length: {len(description)})")
        
        # Test full extraction
        print(f"\n🌍 TESTING FULL EXTRACTION:")
        result = extractor.extract_international_content(sample_ai_response, 'ja')
        
        if result:
            print("✅ Full extraction successful!")
            print(f"   Title: '{result.get('productTitle', 'MISSING')}' ({len(result.get('productTitle', '')) if result.get('productTitle') else 0} chars)")
            bullets_result = result.get('bulletPoints', [])
            print(f"   Bullets: {len(bullets_result)} items")
            if bullets_result:
                print(f"     First: '{bullets_result[0][:60]}...'")
            desc_result = result.get('productDescription', '')
            print(f"   Description: '{desc_result}' ({len(desc_result)} chars)")
        else:
            print("❌ Full extraction failed!")
            
        return True
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_extractor()