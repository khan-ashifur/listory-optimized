"""
Compare German vs Japanese generation architecture to identify differences
"""

import os
import sys
import django

# Add the project path and configure Django
project_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

def compare_architectures():
    """Compare German vs Japanese generation to find architecture differences"""
    
    try:
        from apps.listings.services import ListingGeneratorService
        from apps.core.models import Product
        from django.contrib.auth.models import User
        import json

        service = ListingGeneratorService()
        
        print("🔍 COMPARING GERMAN VS JAPANESE ARCHITECTURE...")
        print("=" * 60)
        
        # Test German generation
        print("🇩🇪 TESTING GERMAN GENERATION:")
        user_de, _ = User.objects.get_or_create(username='test_de_arch', defaults={'email': 'test@amazon.de'})
        product_de = Product.objects.create(
            user=user_de,
            name='Test Kopfhörer',
            description='Test',
            brand_name='TestBrand',
            brand_tone='professional',
            target_platform='amazon',
            marketplace='de',
            marketplace_language='de',
            price=99,
            categories='Electronics',
            features='Test'
        )
        
        result_de = service.generate_listing(product_de.id, 'amazon')
        
        if result_de:
            # Check raw AI data structure for German
            print(f"German A+ length: {len(getattr(result_de, 'amazon_aplus_content', ''))}")
            
            # Check keywords structure
            de_keywords = getattr(result_de, 'amazon_keywords', '')
            de_backend = getattr(result_de, 'amazon_backend_keywords', '')
            print(f"German Keywords: {len(de_keywords.split(',')) if de_keywords else 0} total")
            print(f"German Backend: {len(de_backend)} chars")
        
        product_de.delete()
        
        print("\n" + "=" * 60)
        
        # Test Japanese generation
        print("🇯🇵 TESTING JAPANESE GENERATION:")
        user_jp, _ = User.objects.get_or_create(username='test_jp_arch', defaults={'email': 'test@amazon.co.jp'})
        product_jp = Product.objects.create(
            user=user_jp,
            name='テストイヤホン',
            description='テスト',
            brand_name='TestBrand',
            brand_tone='professional',
            target_platform='amazon',
            marketplace='jp',
            marketplace_language='ja',
            price=12800,
            categories='Electronics',
            features='テスト'
        )
        
        result_jp = service.generate_listing(product_jp.id, 'amazon')
        
        if result_jp:
            print(f"Japanese A+ length: {len(getattr(result_jp, 'amazon_aplus_content', ''))}")
            
            # Check keywords structure
            jp_keywords = getattr(result_jp, 'amazon_keywords', '')
            jp_backend = getattr(result_jp, 'amazon_backend_keywords', '')
            print(f"Japanese Keywords: {len(jp_keywords.split(',')) if jp_keywords else 0} total")
            print(f"Japanese Backend: {len(jp_backend)} chars")
            
            # Debug the keyword content
            print(f"\nKeyword samples:")
            print(f"German keywords (first 100 chars): {de_keywords[:100]}...")
            print(f"Japanese keywords (first 100 chars): {jp_keywords[:100]}...")
            
        product_jp.delete()
        
        print("\n🔍 ARCHITECTURE COMPARISON SUMMARY:")
        print("=" * 50)
        
        if result_de and result_jp:
            de_aplus_len = len(getattr(result_de, 'amazon_aplus_content', ''))
            jp_aplus_len = len(getattr(result_jp, 'amazon_aplus_content', ''))
            
            print(f"A+ Content Length:")
            print(f"  German: {de_aplus_len} chars")
            print(f"  Japanese: {jp_aplus_len} chars")
            print(f"  Match: {'✅' if abs(de_aplus_len - jp_aplus_len) < 5000 else '❌'}")
            
            de_kw_count = len(de_keywords.split(',')) if de_keywords else 0
            jp_kw_count = len(jp_keywords.split(',')) if jp_keywords else 0
            
            print(f"\nKeyword Count:")
            print(f"  German: {de_kw_count} keywords")
            print(f"  Japanese: {jp_kw_count} keywords")
            print(f"  Match: {'✅' if abs(de_kw_count - jp_kw_count) < 10 else '❌'}")
            
            de_backend_len = len(de_backend) if de_backend else 0
            jp_backend_len = len(jp_backend) if jp_backend else 0
            
            print(f"\nBackend Keywords:")
            print(f"  German: {de_backend_len} chars")
            print(f"  Japanese: {jp_backend_len} chars")
            print(f"  Match: {'✅' if abs(de_backend_len - jp_backend_len) < 50 else '❌'}")
            
            # Overall assessment
            issues = []
            if abs(de_aplus_len - jp_aplus_len) >= 5000:
                issues.append("A+ content length mismatch")
            if abs(de_kw_count - jp_kw_count) >= 10:
                issues.append("Keyword count mismatch")
            if abs(de_backend_len - jp_backend_len) >= 50:
                issues.append("Backend keywords mismatch")
                
            if issues:
                print(f"\n❌ ISSUES FOUND:")
                for issue in issues:
                    print(f"  - {issue}")
            else:
                print(f"\n✅ ARCHITECTURE MATCHES!")
                
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    compare_architectures()