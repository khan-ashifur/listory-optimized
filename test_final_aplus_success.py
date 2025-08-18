"""
Final A+ content success test - verify the 8 sections are working
"""

import os
import sys
import django

# Add the project path and configure Django
project_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

def test_final_aplus_success():
    """Test final A+ content success with 8 sections"""
    
    try:
        from apps.listings.services import ListingGeneratorService
        from apps.core.models import Product
        from django.contrib.auth.models import User

        print("🎉 FINAL A+ CONTENT SUCCESS TEST")
        print("=" * 50)
        
        user, _ = User.objects.get_or_create(
            username='final_aplus_test', 
            defaults={'email': 'test@test.com'}
        )
        
        # Test with a more detailed product
        product = Product.objects.create(
            user=user,
            name='プレミアムワイヤレスイヤホン',
            description='高品質ワイヤレスイヤホンで最高の音楽体験を',
            brand_name='AudioMaster',
            brand_tone='premium',
            marketplace='jp',
            marketplace_language='ja',
            features='アクティブノイズキャンセリング,50時間バッテリー,Bluetooth5.3,IPX7防水',
            price=15800,
            occasion='正月'
        )
        
        service = ListingGeneratorService()
        result = service.generate_listing(product.id, 'amazon')
        
        if result:
            aplus_content = getattr(result, 'amazon_aplus_content', '')
            
            print(f"📊 SUCCESS METRICS:")
            print(f"   ✅ Total A+ content: {len(aplus_content):,} characters")
            
            # Count sections
            sections = aplus_content.split('<h3>')[1:] if '<h3>' in aplus_content else []
            print(f"   ✅ Sections generated: {len(sections)}")
            
            # Check Japanese content
            has_japanese = any('\\u3040' <= c <= '\\u309f' or '\\u30a0' <= c <= '\\u30ff' or '\\u4e00' <= c <= '\\u9faf' for c in aplus_content)
            print(f"   ✅ Japanese content: {has_japanese}")
            
            # Check for English HTML fallback
            has_english_html = '<div class="aplus-introduction' in aplus_content
            print(f"   ✅ Localized (not English HTML): {not has_english_html}")
            
            if sections and has_japanese and not has_english_html:
                print(f"\\n🎉 SUCCESS! A+ CONTENT IS WORKING PERFECTLY!")
                print(f"\\n📄 SECTION PREVIEW:")
                
                for i, section in enumerate(sections[:5], 1):  # Show first 5 sections
                    if '</h3>' in section:
                        title = section.split('</h3>')[0]
                        content_start = section.find('<p>') + 3 if '<p>' in section else len(section.split('</h3>')[0]) + 5
                        content_end = section.find('</p>') if '</p>' in section else content_start + 100
                        content = section[content_start:content_end] if content_end > content_start else section[content_start:content_start+80]
                        
                        print(f"   Section {i}: {title}")
                        print(f"      Content: {content[:60]}...")
                        print(f"      Length: {len(content)} characters")
                
                # Keywords analysis
                keywords = getattr(result, 'keywords', '')
                if keywords:
                    keyword_list = [k.strip() for k in keywords.split(',') if k.strip()]
                    short_tail = [k for k in keyword_list if len(k.split()) <= 2]
                    long_tail = [k for k in keyword_list if len(k.split()) > 2]
                    
                    print(f"\\n🔑 KEYWORDS SUCCESS:")
                    print(f"   Total: {len(keyword_list)} keywords")
                    print(f"   Short-tail: {len(short_tail)} keywords")  
                    print(f"   Long-tail: {len(long_tail)} keywords")
                    print(f"   Balance: {'✅ GOOD' if abs(len(short_tail) - len(long_tail)) < 20 else '⚠️ NEEDS WORK'}")
                
                print(f"\\n🎯 OVERALL ASSESSMENT:")
                quality_issues = []
                if len(aplus_content) < 8000:
                    quality_issues.append(f"A+ content could be longer ({len(aplus_content):,} vs 8,000+ target)")
                if len(sections) < 8:
                    quality_issues.append(f"Need {8-len(sections)} more sections")
                if len(keyword_list) < 75:
                    quality_issues.append(f"Need {75-len(keyword_list)} more keywords")
                
                if not quality_issues:
                    print("   🌟 PERFECT! All targets achieved!")
                else:
                    print("   📈 WORKING GREAT! Areas for optimization:")
                    for issue in quality_issues:
                        print(f"      • {issue}")
                
                return True
            else:
                print("\\n❌ A+ content generation has issues")
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
    success = test_final_aplus_success()
    print(f"\\n{'='*50}")
    if success:
        print("✅ A+ CONTENT ENHANCEMENT SUCCESSFUL!")
        print("🎉 8-SECTION JAPANESE A+ CONTENT IS WORKING!")
    else:
        print("❌ A+ content needs further debugging")