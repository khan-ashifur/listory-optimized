"""
Analyze keyword issue - why too many short-tail, not enough long-tail
"""

import os
import sys
import django

# Add the project path and configure Django
project_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

def analyze_keyword_issue():
    """Analyze why keywords aren't properly balanced"""
    
    try:
        from apps.listings.services import ListingGeneratorService
        from apps.core.models import Product
        from django.contrib.auth.models import User

        print("🔍 ANALYZING KEYWORD ISSUE...")
        print("=" * 50)
        
        # Test with a US product first (should work properly)
        user, _ = User.objects.get_or_create(username='keyword_test', defaults={'email': 'test@test.com'})
        
        # US Test
        product_us = Product.objects.create(
            user=user,
            name='Wireless Headphones',
            description='High quality audio',
            brand_name='SoundTech',
            marketplace='com',
            marketplace_language='en'
        )
        
        service = ListingGeneratorService()
        result_us = service.generate_listing(product_us.id, 'amazon')
        
        if result_us:
            keywords_us = getattr(result_us, 'keywords', '')
            if keywords_us:
                kw_list_us = [k.strip() for k in keywords_us.split(',') if k.strip()]
                short_us = [k for k in kw_list_us if len(k.split()) <= 2]
                long_us = [k for k in kw_list_us if len(k.split()) > 2]
                
                print(f"🇺🇸 US RESULTS:")
                print(f"   Total: {len(kw_list_us)}")
                print(f"   Short-tail: {len(short_us)} ({len(short_us)/len(kw_list_us)*100:.1f}%)")
                print(f"   Long-tail: {len(long_us)} ({len(long_us)/len(kw_list_us)*100:.1f}%)")
                
                print(f"\n   US Long-tail examples:")
                for i, kw in enumerate(long_us[:3], 1):
                    print(f"     {i}. '{kw}' ({len(kw.split())} words)")
        
        product_us.delete()
        
        # Japanese Test  
        product_jp = Product.objects.create(
            user=user,
            name='ワイヤレスイヤホン',
            description='高音質オーディオ',
            brand_name='SoundTech',
            marketplace='jp',
            marketplace_language='ja'
        )
        
        result_jp = service.generate_listing(product_jp.id, 'amazon')
        
        if result_jp:
            keywords_jp = getattr(result_jp, 'keywords', '')
            if keywords_jp:
                kw_list_jp = [k.strip() for k in keywords_jp.split(',') if k.strip()]
                short_jp = [k for k in kw_list_jp if len(k.split()) <= 2]
                long_jp = [k for k in kw_list_jp if len(k.split()) > 2]
                
                print(f"\n🇯🇵 JAPANESE RESULTS:")
                print(f"   Total: {len(kw_list_jp)}")  
                print(f"   Short-tail: {len(short_jp)} ({len(short_jp)/len(kw_list_jp)*100:.1f}%)")
                print(f"   Long-tail: {len(long_jp)} ({len(long_jp)/len(kw_list_jp)*100:.1f}%)")
                
                print(f"\n   JP Long-tail examples:")
                for i, kw in enumerate(long_jp[:3], 1):
                    print(f"     {i}. '{kw}' ({len(kw.split())} words)")
                
                print(f"\n   JP Short-tail examples:")
                for i, kw in enumerate(short_jp[:10], 1):
                    print(f"     {i}. '{kw}' ({len(kw.split())} words)")
        
        product_jp.delete()
        
        print(f"\n🎯 ANALYSIS:")
        print(f"   The issue appears to be that Japanese keywords are")
        print(f"   being generated mostly as single words or brand names")
        print(f"   instead of longer descriptive phrases")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    analyze_keyword_issue()