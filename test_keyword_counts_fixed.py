"""
Test keyword counts are fixed for international markets (German and Japanese)
"""

import os
import sys
import django

# Add the project path and configure Django
project_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

def test_keyword_counts_fixed():
    """Test that German and Japanese markets show proper keyword counts"""
    
    try:
        from apps.listings.services import ListingGeneratorService
        from apps.core.models import Product
        from django.contrib.auth.models import User

        print("🔍 TESTING FIXED KEYWORD COUNTS...")
        print("=" * 60)
        
        markets_to_test = [
            ('de', 'de', 'German', 'Test Präzisionsgerät'),
            ('jp', 'ja', 'Japanese', 'テストイヤホン')
        ]
        
        service = ListingGeneratorService()
        results = {}
        
        for marketplace, language, market_name, product_name in markets_to_test:
            print(f"\n🌍 TESTING {market_name.upper()} MARKET ({marketplace}):")
            print("-" * 40)
            
            user, _ = User.objects.get_or_create(
                username=f'test_{marketplace}_keywords', 
                defaults={'email': f'test@amazon.{marketplace}'}
            )
            
            product = Product.objects.create(
                user=user,
                name=product_name,
                description='Testing comprehensive keywords',
                brand_name='TestBrand',
                brand_tone='professional',
                target_platform='amazon',
                marketplace=marketplace,
                marketplace_language=language,
                price=12800 if marketplace == 'jp' else 99,
                categories='Electronics,Audio',
                features='Test comprehensive keywords'
            )
            
            result = service.generate_listing(product.id, 'amazon')
            
            if result:
                # Check both keyword fields
                keywords_field = getattr(result, 'keywords', '')
                amazon_keywords_field = getattr(result, 'amazon_keywords', '')
                backend_keywords_field = getattr(result, 'amazon_backend_keywords', '')
                
                # Count keywords
                if keywords_field:
                    keyword_list = [k.strip() for k in keywords_field.split(',') if k.strip()]
                    short_tail = [k for k in keyword_list if len(k.split()) <= 2]
                    long_tail = [k for k in keyword_list if len(k.split()) > 2]
                    
                    print(f"📊 {market_name} KEYWORD RESULTS:")
                    print(f"   ✅ keywords field: {len(keywords_field)} chars, {len(keyword_list)} total keywords")
                    print(f"   ✅ amazon_keywords field: {len(amazon_keywords_field)} chars")
                    print(f"   ✅ amazon_backend_keywords: {len(backend_keywords_field)} chars")
                    print(f"   📈 Short-tail: {len(short_tail)} keywords")
                    print(f"   📈 Long-tail: {len(long_tail)} keywords")
                    print(f"   🎯 Fields match: {'✅' if keywords_field == amazon_keywords_field else '❌'}")
                    
                    # Check if we have comprehensive keywords (79+ total expected)
                    is_comprehensive = len(keyword_list) >= 75
                    print(f"   🏆 Comprehensive: {'✅ EXCELLENT' if is_comprehensive else '❌ NEEDS MORE'} ({len(keyword_list)}/79+ expected)")
                    
                    results[market_name] = {
                        'total_keywords': len(keyword_list),
                        'short_tail': len(short_tail),
                        'long_tail': len(long_tail),
                        'fields_match': keywords_field == amazon_keywords_field,
                        'comprehensive': is_comprehensive,
                        'backend_chars': len(backend_keywords_field)
                    }
                    
                    # Show sample keywords
                    print(f"   📝 Sample keywords: {', '.join(keyword_list[:3])}...")
                    
                else:
                    print(f"❌ No keywords generated for {market_name}")
                    results[market_name] = {'total_keywords': 0, 'comprehensive': False}
            else:
                print(f"❌ Failed to generate listing for {market_name}")
                results[market_name] = {'total_keywords': 0, 'comprehensive': False}
            
            # Cleanup
            product.delete()
        
        # Summary
        print(f"\n🎯 KEYWORD FIX SUMMARY:")
        print("=" * 50)
        
        total_success = 0
        for market_name, data in results.items():
            status = "✅ FIXED" if data.get('comprehensive', False) and data.get('total_keywords', 0) >= 75 else "❌ STILL BROKEN"
            print(f"   {market_name}: {status} ({data.get('total_keywords', 0)} keywords)")
            if data.get('comprehensive', False) and data.get('total_keywords', 0) >= 75:
                total_success += 1
        
        all_fixed = total_success == len(markets_to_test)
        print(f"\n🏁 OVERALL: {'🎉 ALL MARKETS FIXED!' if all_fixed else f'🔧 {total_success}/{len(markets_to_test)} MARKETS WORKING'}")
        
        if all_fixed:
            print(f"✅ User's issue resolved: Keywords now show 75+ total instead of '1 Short-tail 1 Long-tail 1 Backend Terms only'")
        
        return all_fixed
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_keyword_counts_fixed()
    print(f"\n{'🎌 KEYWORDS FIXED FOR ALL MARKETS!' if success else '🔧 STILL NEEDS WORK'}")