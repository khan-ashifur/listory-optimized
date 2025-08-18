"""
Check what A+ content is actually being generated
"""

import os
import sys
import django

# Add the project path and configure Django
project_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

def check_actual_aplus_content():
    """Check what A+ content is actually being generated"""
    
    try:
        from apps.listings.services import ListingGeneratorService
        from apps.core.models import Product
        from django.contrib.auth.models import User

        print("🔍 CHECKING ACTUAL A+ CONTENT")
        print("=" * 40)
        
        user, _ = User.objects.get_or_create(
            username='check_aplus', 
            defaults={'email': 'test@test.com'}
        )
        
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
            
            print(f"📄 ACTUAL A+ CONTENT ({len(aplus_content)} chars):")
            print("=" * 40)
            print(aplus_content)
            print("=" * 40)
            
            # Detailed analysis
            sections = aplus_content.split('<h3>')[1:] if '<h3>' in aplus_content else []
            print(f"\\n📊 ANALYSIS:")
            print(f"   Sections: {len(sections)}")
            print(f"   Total length: {len(aplus_content)} chars")
            
            # Check for different types of content
            has_html_tags = bool('<h3>' in aplus_content and '</h3>' in aplus_content)
            has_japanese_chars = any('\\u3040' <= c <= '\\u309f' or '\\u30a0' <= c <= '\\u30ff' or '\\u4e00' <= c <= '\\u9faf' for c in aplus_content)
            has_english_html_template = '<div class="aplus-introduction' in aplus_content
            
            print(f"   Has HTML sections: {has_html_tags}")
            print(f"   Has Japanese chars: {has_japanese_chars}")  
            print(f"   Is English template: {has_english_html_template}")
            
            if sections:
                print(f"\\n📋 SECTION BREAKDOWN:")
                for i, section in enumerate(sections, 1):
                    if '</h3>' in section:
                        title = section.split('</h3>')[0]
                        content_part = section.split('</h3>', 1)[1] if '</h3>' in section else section
                        
                        # Extract content between <p> tags if they exist
                        if '<p>' in content_part and '</p>' in content_part:
                            p_start = content_part.find('<p>') + 3
                            p_end = content_part.find('</p>')
                            content = content_part[p_start:p_end] if p_end > p_start else content_part[:100]
                        else:
                            content = content_part[:100]
                        
                        content_has_japanese = any('\\u3040' <= c <= '\\u309f' or '\\u30a0' <= c <= '\\u30ff' or '\\u4e00' <= c <= '\\u9faf' for c in content)
                        
                        print(f"   Section {i}: {title}")
                        print(f"      Content: {content[:60]}...")
                        print(f"      Has Japanese: {content_has_japanese}")
                        print(f"      Length: {len(content)} chars")
            
        else:
            print("❌ Failed to generate listing")
        
        product.delete()
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_actual_aplus_content()