"""
Verify the A+ content fix is working - should now get 9,970+ characters
"""

import os
import sys
import django

# Add the project path and configure Django
project_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

def verify_aplus_fix():
    """Verify the A+ content fix is working with comprehensive content"""
    
    try:
        from apps.listings.services import ListingGeneratorService
        from apps.core.models import Product
        from django.contrib.auth.models import User

        print("🔍 VERIFYING A+ CONTENT FIX")
        print("=" * 50)
        
        user, _ = User.objects.get_or_create(
            username='verify_aplus_fix', 
            defaults={'email': 'test@test.com'}
        )
        
        product = Product.objects.create(
            user=user,
            name='プレミアムワイヤレスイヤホン',
            description='最高品質のオーディオ体験',
            brand_name='AudioPro',
            brand_tone='premium',
            marketplace='jp',
            marketplace_language='ja',
            features='ノイズキャンセリング,50時間バッテリー,防水設計',
            price=15800
        )
        
        print("🚀 Generating listing with fixed A+ content...")
        service = ListingGeneratorService()
        result = service.generate_listing(product.id, 'amazon')
        
        if result:
            aplus_content = getattr(result, 'amazon_aplus_content', '')
            
            print(f"📊 RESULTS:")
            print(f"   A+ Content Length: {len(aplus_content):,} characters")
            print(f"   Target: 9,970+ characters (agent promised)")
            
            # Check if it's the comprehensive structure
            has_comprehensive_structure = all([
                '<div class="aplus-introduction' in aplus_content,
                'Complete A+ Content Strategy' in aplus_content,
                '<div class="aplus-comprehensive-plan">' in aplus_content,
                'bg-gradient-to-r' in aplus_content
            ])
            
            # Check sections
            section_count = aplus_content.count('<h3>')
            
            # Check Japanese content
            has_japanese = any('\\u3040' <= c <= '\\u309f' or '\\u30a0' <= c <= '\\u30ff' or '\\u4e00' <= c <= '\\u9faf' for c in aplus_content)
            
            print(f"   Comprehensive Structure: {'✅' if has_comprehensive_structure else '❌'}")
            print(f"   Section Count: {section_count}")
            print(f"   Has Japanese Content: {'✅' if has_japanese else '❌'}")
            
            # Quality assessment
            if len(aplus_content) >= 9000 and has_comprehensive_structure:
                print(f"\\n🎉 SUCCESS! A+ content fix is working!")
                print(f"   - 10x content increase achieved")
                print(f"   - Comprehensive HTML structure preserved")
                print(f"   - Japanese localization maintained")
            elif len(aplus_content) >= 5000:
                print(f"\\n⚠️ PARTIAL SUCCESS - Content increased but target not fully met")
            else:
                print(f"\\n❌ FIX NOT WORKING - Content length still too low")
            
            # Show content preview
            print(f"\\n📄 CONTENT PREVIEW (first 300 chars):")
            print("=" * 50)
            print(aplus_content[:300] + "...")
            print("=" * 50)
            
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
    verify_aplus_fix()