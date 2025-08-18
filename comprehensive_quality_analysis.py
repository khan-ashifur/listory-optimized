"""
Comprehensive quality analysis - find all issues and fix to 10/10
"""

import os
import sys
import django

# Add the project path and configure Django
project_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

def comprehensive_quality_analysis():
    """Comprehensive analysis of all quality issues"""
    
    try:
        from apps.listings.services import ListingGeneratorService
        from apps.core.models import Product
        from django.contrib.auth.models import User

        print("🔍 COMPREHENSIVE QUALITY ANALYSIS - FIXING TO 10/10")
        print("=" * 70)
        
        # Test multiple markets
        markets_to_test = [
            ('jp', 'ja', 'Japanese', 'プレミアムワイヤレスイヤホン'),
            ('de', 'de', 'German', 'Premium Kopfhörer'),
        ]
        
        service = ListingGeneratorService()
        
        for marketplace, language, market_name, product_name in markets_to_test:
            print(f"\n🌍 ANALYZING {market_name.upper()} MARKET QUALITY:")
            print("-" * 50)
            
            user, _ = User.objects.get_or_create(
                username=f'quality_{marketplace}', 
                defaults={'email': f'test@amazon.{marketplace}'}
            )
            
            product = Product.objects.create(
                user=user,
                name=product_name,
                description='高品質テスト商品' if marketplace == 'jp' else 'Premium Test Product',
                brand_name='PremiumBrand',
                brand_tone='professional',
                target_platform='amazon',
                marketplace=marketplace,
                marketplace_language=language,
                price=12800 if marketplace == 'jp' else 99,
                categories='Electronics,Audio,Headphones',
                features='ノイズキャンセリング,30時間バッテリー,Bluetooth5.3' if marketplace == 'jp' else 'Noise Cancelling,30h Battery,Bluetooth 5.3',
                occasion='正月' if marketplace == 'jp' else 'Christmas'
            )
            
            result = service.generate_listing(product.id, 'amazon')
            
            if result:
                # COMPREHENSIVE ANALYSIS
                print(f"📊 {market_name} QUALITY ANALYSIS:")
                
                # 1. KEYWORD ANALYSIS
                keywords = getattr(result, 'keywords', '')
                amazon_keywords = getattr(result, 'amazon_keywords', '')
                backend_keywords = getattr(result, 'amazon_backend_keywords', '')
                
                if keywords:
                    keyword_list = [k.strip() for k in keywords.split(',') if k.strip()]
                    short_tail = [k for k in keyword_list if len(k.split()) <= 2]
                    long_tail = [k for k in keyword_list if len(k.split()) > 2]
                    
                    print(f"   🔑 KEYWORDS:")
                    print(f"      Total: {len(keyword_list)} (Target: 75+ for comprehensive)")
                    print(f"      Short-tail: {len(short_tail)} (Target: 35-40)")
                    print(f"      Long-tail: {len(long_tail)} (Target: 35-40)")
                    print(f"      Backend chars: {len(backend_keywords)} (Target: 240+ chars)")
                    print(f"      amazon_keywords populated: {'✅' if amazon_keywords else '❌'}")
                    
                    # Quality assessment
                    keyword_quality = "❌ POOR"
                    if len(keyword_list) >= 75 and len(long_tail) >= 30:
                        keyword_quality = "✅ EXCELLENT"
                    elif len(keyword_list) >= 40 and len(long_tail) >= 15:
                        keyword_quality = "⚠️ FAIR"
                    
                    print(f"      Quality: {keyword_quality}")
                    
                    # Show samples
                    native_keywords = []
                    if marketplace == 'jp':
                        native_keywords = [k for k in keyword_list if any('\u3040' <= c <= '\u309f' or '\u30a0' <= c <= '\u30ff' or '\u4e00' <= c <= '\u9faf' for c in k)]
                    elif marketplace == 'de':
                        native_keywords = [k for k in keyword_list if any(c in 'äöüßÄÖÜ' for c in k)]
                    
                    print(f"      Native {market_name} keywords: {len(native_keywords)} out of {len(keyword_list)}")
                    if native_keywords:
                        print(f"      Samples: {', '.join(native_keywords[:3])}...")
                
                # 2. A+ CONTENT ANALYSIS
                aplus_content = getattr(result, 'amazon_aplus_content', '')
                print(f"\n   📄 A+ CONTENT:")
                print(f"      Length: {len(aplus_content)} chars")
                print(f"      Target: 25,000+ chars (German baseline)")
                
                if aplus_content:
                    # Check language
                    if marketplace == 'jp':
                        has_japanese = any('\u3040' <= c <= '\u309f' or '\u30a0' <= c <= '\u30ff' or '\u4e00' <= c <= '\u9faf' for c in aplus_content)
                        has_english_structure = any(word in aplus_content.lower() for word in ['div', 'class=', 'bg-gradient'])
                        print(f"      Japanese content: {'✅' if has_japanese else '❌'}")
                        print(f"      English HTML structure: {'❌ BAD' if has_english_structure else '✅ CLEAN'}")
                    elif marketplace == 'de':
                        has_german = any(c in 'äöüßÄÖÜ' for c in aplus_content)
                        print(f"      German content: {'✅' if has_german else '❌'}")
                    
                    # Count sections
                    section_count = aplus_content.count('<h3>')
                    print(f"      Sections: {section_count} (Target: 8+ sections)")
                    
                    # Quality assessment
                    aplus_quality = "❌ POOR"
                    if len(aplus_content) >= 25000 and section_count >= 8:
                        aplus_quality = "✅ EXCELLENT"
                    elif len(aplus_content) >= 15000 and section_count >= 6:
                        aplus_quality = "⚠️ FAIR"
                    
                    print(f"      Quality: {aplus_quality}")
                    
                    # Show sample
                    print(f"      Sample: {aplus_content[:150]}...")
                
                # 3. TITLE & BULLETS ANALYSIS
                title = getattr(result, 'title', '')
                bullets = getattr(result, 'bullet_points', '')
                description = getattr(result, 'long_description', '')
                
                print(f"\n   📝 CONTENT:")
                print(f"      Title: {len(title)} chars")
                print(f"      Bullets: {len(bullets)} chars")
                print(f"      Description: {len(description)} chars")
                
                if marketplace == 'jp':
                    title_japanese = any('\u3040' <= c <= '\u309f' or '\u30a0' <= c <= '\u30ff' or '\u4e00' <= c <= '\u9faf' for c in title)
                    bullets_japanese = any('\u3040' <= c <= '\u309f' or '\u30a0' <= c <= '\u30ff' or '\u4e00' <= c <= '\u9faf' for c in bullets)
                    print(f"      Title in Japanese: {'✅' if title_japanese else '❌'}")
                    print(f"      Bullets in Japanese: {'✅' if bullets_japanese else '❌'}")
                
                # 4. OVERALL ASSESSMENT
                issues = []
                if len(keyword_list if keywords else []) < 75:
                    issues.append(f"Need {75 - len(keyword_list if keywords else [])} more keywords")
                if len(long_tail if keywords else []) < 30:
                    issues.append(f"Need {30 - len(long_tail if keywords else [])} more long-tail keywords")
                if len(aplus_content) < 25000:
                    issues.append(f"A+ content needs {25000 - len(aplus_content)} more chars")
                if section_count < 8:
                    issues.append(f"A+ content needs {8 - section_count} more sections")
                
                print(f"\n   🎯 ISSUES TO FIX ({len(issues)} total):")
                for i, issue in enumerate(issues, 1):
                    print(f"      {i}. {issue}")
                
                if not issues:
                    print(f"   🎉 {market_name} MARKET: PERFECT QUALITY!")
                else:
                    print(f"   🔧 {market_name} MARKET: NEEDS IMPROVEMENT")
            
            else:
                print(f"❌ Failed to generate listing for {market_name}")
            
            # Cleanup
            product.delete()
        
        print(f"\n🎯 NEXT STEPS TO ACHIEVE 10/10:")
        print("1. Restore comprehensive keyword generation (75+ total)")
        print("2. Ensure proper keyword balance (35-40 short + 35-40 long)")
        print("3. Generate full A+ content (25,000+ chars, 8+ sections)")
        print("4. Maintain proper localization for each market")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    comprehensive_quality_analysis()