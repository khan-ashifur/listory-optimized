"""
Test current broken state - keywords and A+ content issues
"""

import os
import sys
import django

# Add the project path and configure Django
project_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

def test_current_broken_state():
    """Test what's currently broken with keywords and A+ content"""
    
    try:
        from apps.listings.services import ListingGeneratorService
        from apps.core.models import Product
        from django.contrib.auth.models import User
        import json

        print("🔍 TESTING CURRENT BROKEN STATE...")
        print("=" * 60)
        
        # Test Japanese market
        user, _ = User.objects.get_or_create(username='test_broken', defaults={'email': 'test@amazon.co.jp'})
        product = Product.objects.create(
            user=user,
            name='ワイヤレスイヤホン',
            description='高品質オーディオ',
            brand_name='SoundTech',
            brand_tone='professional',
            target_platform='amazon',
            marketplace='jp',
            marketplace_language='ja',
            price=9800,
            categories='Electronics,Audio',
            features='ノイズキャンセリング'
        )
        
        service = ListingGeneratorService()
        result = service.generate_listing(product.id, 'amazon')
        
        if result:
            print("📊 GENERATED LISTING ANALYSIS:")
            print("-" * 40)
            
            # Check keywords
            keywords = getattr(result, 'keywords', '')
            amazon_keywords = getattr(result, 'amazon_keywords', '')
            
            if keywords:
                keyword_list = [k.strip() for k in keywords.split(',') if k.strip()]
                
                # Analyze keyword types - PROPERLY
                short_tail = []
                long_tail = []
                
                for kw in keyword_list:
                    word_count = len(kw.split())
                    if word_count <= 2:
                        short_tail.append(kw)
                    else:
                        long_tail.append(kw)
                
                print(f"🔍 KEYWORD BREAKDOWN:")
                print(f"   Total keywords: {len(keyword_list)}")
                print(f"   Short-tail (1-2 words): {len(short_tail)}")
                print(f"   Long-tail (3+ words): {len(long_tail)}")
                print(f"   amazon_keywords populated: {'✅' if amazon_keywords else '❌'}")
                
                print(f"\n📝 SHORT-TAIL EXAMPLES (first 5):")
                for i, kw in enumerate(short_tail[:5], 1):
                    print(f"   {i}. '{kw}' ({len(kw.split())} words)")
                
                print(f"\n📝 LONG-TAIL EXAMPLES (first 5):")
                if long_tail:
                    for i, kw in enumerate(long_tail[:5], 1):
                        print(f"   {i}. '{kw}' ({len(kw.split())} words)")
                else:
                    print("   ❌ NO LONG-TAIL KEYWORDS FOUND!")
                
                # Check if keywords are in Japanese
                japanese_kws = [kw for kw in keyword_list[:10] if any('\u3040' <= c <= '\u309f' or '\u30a0' <= c <= '\u30ff' or '\u4e00' <= c <= '\u9faf' for c in kw)]
                print(f"\n🇯🇵 JAPANESE KEYWORDS: {len(japanese_kws)} out of first 10")
                
            # Check A+ content
            aplus_content = getattr(result, 'amazon_aplus_content', '')
            print(f"\n📄 A+ CONTENT ANALYSIS:")
            print(f"   Length: {len(aplus_content)} chars")
            
            if aplus_content:
                # Check if A+ content is in English or Japanese
                has_japanese = any('\u3040' <= c <= '\u309f' or '\u30a0' <= c <= '\u30ff' or '\u4e00' <= c <= '\u9faf' for c in aplus_content[:500])
                has_english_headers = 'section' in aplus_content.lower() or 'hero' in aplus_content.lower()
                
                print(f"   Has Japanese text: {'✅' if has_japanese else '❌'}")
                print(f"   Has English structure words: {'✅' if has_english_headers else '❌'}")
                
                # Show sample of A+ content
                print(f"\n   A+ Content sample (first 200 chars):")
                print(f"   {aplus_content[:200]}...")
                
                # Count sections
                section_count = aplus_content.count('section')
                print(f"\n   Section mentions: {section_count}")
                
            # Check title and bullets
            title = getattr(result, 'title', '')
            bullets = getattr(result, 'bullet_points', '')
            
            print(f"\n🎯 OTHER FIELDS:")
            print(f"   Title in Japanese: {'✅' if any('\u3040' <= c <= '\u309f' or '\u30a0' <= c <= '\u30ff' or '\u4e00' <= c <= '\u9faf' for c in title) else '❌'}")
            print(f"   Bullets in Japanese: {'✅' if any('\u3040' <= c <= '\u309f' or '\u30a0' <= c <= '\u30ff' or '\u4e00' <= c <= '\u9faf' for c in bullets) else '❌'}")
            
        else:
            print("❌ Failed to generate listing")
        
        product.delete()
        
        print("\n🚨 ISSUES IDENTIFIED:")
        print("1. Keywords only showing short-tail, no long-tail")
        print("2. A+ content in English instead of Japanese")
        print("3. Keyword categorization broken")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_current_broken_state()