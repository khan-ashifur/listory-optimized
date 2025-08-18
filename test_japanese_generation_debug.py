"""
🇯🇵 DEBUG JAPANESE LISTING GENERATION
Test exactly what AI is generating vs what we expect
"""

import os
import sys
import django

# Add the project path and configure Django
project_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

def debug_japanese_generation():
    """Debug Japanese listing generation step by step"""
    
    print("🇯🇵 DEBUGGING JAPANESE LISTING GENERATION")
    print("=" * 60)
    
    try:
        from apps.listings.services import ListingGeneratorService
        from apps.core.models import Product
        from django.contrib.auth.models import User
        
        # Create test user and product
        user, _ = User.objects.get_or_create(username='debug_jp', defaults={'email': 'debug@amazon.co.jp'})
        product = Product.objects.create(
            user=user,
            name='TechSound ワイヤレスイヤホン',
            description='高品質ワイヤレスイヤホン',
            brand_name='TechSound', 
            brand_tone='professional',
            target_platform='amazon',
            marketplace='jp',
            marketplace_language='ja',
            price=12800,
            occasion='正月',
            categories='Electronics,Audio',
            features='ノイズキャンセリング,30時間バッテリー,Bluetooth5.3'
        )
        
        service = ListingGeneratorService()
        
        # Get the prompt that will be sent to AI
        print("🤖 CHECKING AI PROMPT STRUCTURE:")
        print("-" * 40)
        
        # Manually check each format component
        jp_title = service.get_marketplace_title_format('jp', 'TechSound')
        print(f"✅ Title format: {len(jp_title)} chars")
        
        jp_bullets = service.get_marketplace_bullet_format('jp', 1) 
        print(f"✅ Bullet format: {len(jp_bullets)} chars")
        
        jp_desc = service.get_marketplace_description_format('jp', 'professional')
        print(f"✅ Description format: {len(jp_desc)} chars")
        
        # Check if Japanese A+ content is included
        from apps.listings.international_localization_optimizer import InternationalLocalizationOptimizer
        intl_optimizer = InternationalLocalizationOptimizer()
        jp_aplus = intl_optimizer.get_aplus_content_enhancement('jp', 'ja')
        print(f"✅ A+ content format: {len(jp_aplus)} chars")
        
        # Test actual generation
        print(f"\n🚀 GENERATING JAPANESE LISTING:")
        print("-" * 40)
        
        result = service.generate_listing(product.id, 'amazon')
        
        if result:
            # Check what we got back
            title = getattr(result, 'amazon_title', 'NO TITLE')
            bullets = getattr(result, 'amazon_bullets', [])
            description = getattr(result, 'amazon_description', 'NO DESCRIPTION')
            aplus = getattr(result, 'amazon_aplus_content', 'NO A+ CONTENT')
            
            print(f"📝 GENERATED CONTENT ANALYSIS:")
            print(f"   Title: {len(title)} chars - {title[:50]}...")
            print(f"   Bullets: {len(bullets)} items")
            if bullets:
                print(f"   First bullet: {bullets[0][:50]}...")
            print(f"   Description: {len(description)} chars - {description[:50]}...")
            print(f"   A+ Content: {len(aplus)} chars")
            
            # Check for Japanese content
            print(f"\n🔍 JAPANESE CONTENT VALIDATION:")
            print(f"   Title has Japanese chars: {'Yes' if any(ord(char) > 127 for char in title) else 'No'}")
            print(f"   Description has Japanese chars: {'Yes' if any(ord(char) > 127 for char in description) else 'No'}")
            
            # Check for expected Japanese elements
            japanese_checks = {
                'Title has trust signals': any(word in title for word in ['正規品', '安心', '保証']),
                'Title has Japanese product terms': any(word in title for word in ['ワイヤレス', 'イヤホン', 'バッテリー']),
                'Description has keigo': any(word in description for word in ['です', 'ます', 'ございます']),
                'Description has technical specs': any(word in description for word in ['30時間', '-35dB', 'Bluetooth5.3']),
                'A+ content present': 'section1_hero' in aplus or 'hero' in aplus.lower()
            }
            
            for check, result in japanese_checks.items():
                print(f"   {'✅' if result else '❌'} {check}")
            
            success_rate = sum(japanese_checks.values()) / len(japanese_checks) * 100
            print(f"\n🎌 JAPANESE QUALITY: {success_rate:.1f}%")
            
            if success_rate >= 80:
                print("🎉 JAPANESE GENERATION SUCCESS!")
                return True
            else:
                print("⚠️ JAPANESE GENERATION NEEDS IMPROVEMENT")
                return False
        else:
            print("❌ NO RESULT RETURNED")
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
    success = debug_japanese_generation()
    print(f"\n{'🏆 DEBUG COMPLETE' if success else '🔧 NEEDS FIXING'}")