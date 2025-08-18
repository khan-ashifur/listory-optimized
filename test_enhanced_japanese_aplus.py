"""
Test enhanced Japanese A+ content with 8 sections
"""

import os
import sys
import django

# Add the project path and configure Django
project_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

def test_enhanced_japanese_aplus():
    """Test enhanced Japanese A+ content"""
    
    try:
        from apps.listings.services import ListingGeneratorService
        from apps.core.models import Product
        from django.contrib.auth.models import User
        import re

        # Test enhanced Japanese A+ content
        user, _ = User.objects.get_or_create(username='test_enhanced_jp', defaults={'email': 'test@amazon.co.jp'})
        product = Product.objects.create(
            user=user,
            name='プレミアムワイヤレスイヤホン',
            description='高品質ノイズキャンセリング機能付き',
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

        print('🇯🇵 TESTING ENHANCED JAPANESE A+ CONTENT...')
        service = ListingGeneratorService()
        result = service.generate_listing(product.id, 'amazon')

        if result:
            jp_aplus = getattr(result, 'amazon_aplus_content', '')
            print(f'📊 ENHANCED JAPANESE A+ CONTENT:')
            print(f'   Length: {len(jp_aplus)} chars')
            print(f'   Target: 25,000+ chars (similar to German)')
            print(f'   Achievement: {"✅" if len(jp_aplus) > 25000 else "❌"} {"FULL LENGTH" if len(jp_aplus) > 25000 else "NEEDS MORE"}')
            
            # Count sections
            sections = len(re.findall(r'section[1-8]', jp_aplus))
            hero_count = jp_aplus.count('hero')
            features_count = jp_aplus.count('features')  
            trust_count = jp_aplus.count('trust')
            faqs_count = jp_aplus.count('faqs')
            testimonials_count = jp_aplus.count('testimonials')
            whats_in_box_count = jp_aplus.count('whats-in-box')
            usage_count = jp_aplus.count('usage')
            comparison_count = jp_aplus.count('comparison')
            
            print(f'\n🗾 JAPANESE A+ SECTIONS:')
            print(f'   Total sections found: {sections}')
            print(f'   Hero: {hero_count}')
            print(f'   Features: {features_count}')  
            print(f'   Trust: {trust_count}')
            print(f'   Usage: {usage_count}')
            print(f'   Comparison: {comparison_count}')
            print(f'   Testimonials: {testimonials_count}')
            print(f'   Whats in box: {whats_in_box_count}')
            print(f'   FAQs: {faqs_count}')
            
            expected_sections = 8
            actual_sections = sections
            completeness = (actual_sections / expected_sections) * 100 if expected_sections > 0 else 0
            print(f'\n🎌 A+ CONTENT COMPLETENESS: {completeness:.1f}% ({actual_sections}/{expected_sections} sections)')
            
            if len(jp_aplus) > 25000:
                print('\n🎉 SUCCESS: Japanese A+ content now matches German comprehensiveness!')
                return True
            else:
                print(f'\n⚠️ Still short: Need {25000 - len(jp_aplus)} more chars')
                return False
        else:
            print('❌ No Japanese result generated')
            return False

    except Exception as e:
        print(f'❌ ERROR: {e}')
        import traceback
        traceback.print_exc()
        return False
    finally:
        try:
            product.delete()
        except:
            pass

if __name__ == "__main__":
    success = test_enhanced_japanese_aplus()
    print(f"\n{'🎌 JAPANESE A+ CONTENT ENHANCED!' if success else '🔧 NEEDS MORE WORK'}")