"""
Test enhanced A+ content generation with 8 comprehensive sections
"""

import os
import sys
import django

# Add the project path and configure Django
project_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

def test_enhanced_aplus_generation():
    """Test enhanced A+ content with 8 comprehensive sections"""
    
    try:
        from apps.listings.services import ListingGeneratorService
        from apps.core.models import Product
        from django.contrib.auth.models import User

        print("🚀 TESTING ENHANCED A+ CONTENT GENERATION (8 SECTIONS)")
        print("=" * 60)
        
        # Test Japanese market to verify localization
        user, _ = User.objects.get_or_create(
            username='test_enhanced_aplus', 
            defaults={'email': 'test@amazon.jp'}
        )
        
        product = Product.objects.create(
            user=user,
            name='プレミアムワイヤレスイヤホン',
            description='最高品質のワイヤレスイヤホンで究極の音楽体験を',
            brand_name='SoundMaster',
            brand_tone='premium',
            target_platform='amazon',
            marketplace='jp',
            marketplace_language='ja',
            price=15800,
            categories='Electronics,Audio,Headphones',
            features='アクティブノイズキャンセリング,50時間バッテリー,Bluetooth5.3,IPX7防水,高解像度コーデック対応,タッチコントロール',
            occasion='正月'
        )
        
        service = ListingGeneratorService()
        result = service.generate_listing(product.id, 'amazon')
        
        if result:
            # Analyze A+ content quality
            aplus_content = getattr(result, 'amazon_aplus_content', '')
            
            print(f"📊 ENHANCED A+ CONTENT ANALYSIS:")
            print(f"   Length: {len(aplus_content):,} characters")
            print(f"   Target: 25,000+ characters for 10/10 quality")
            
            # Check if we have Japanese content
            has_japanese = any('\\u3040' <= c <= '\\u309f' or '\\u30a0' <= c <= '\\u30ff' or '\\u4e00' <= c <= '\\u9faf' for c in aplus_content)
            
            # Count sections by counting <h3> tags (our section headers)
            section_count = aplus_content.count('<h3>')
            
            print(f"   Sections: {section_count} (Target: 8+ sections)")
            print(f"   Japanese content: {'✅' if has_japanese else '❌'}")
            print(f"   Average chars per section: {len(aplus_content) // section_count if section_count > 0 else 0:,}")
            
            # Quality assessment
            quality_score = "❌ POOR (2/10)"
            if len(aplus_content) >= 25000 and section_count >= 8:
                quality_score = "✅ EXCELLENT (10/10)"
            elif len(aplus_content) >= 20000 and section_count >= 7:
                quality_score = "🟡 VERY GOOD (8/10)"
            elif len(aplus_content) >= 15000 and section_count >= 6:
                quality_score = "⚠️ GOOD (6/10)" 
            elif len(aplus_content) >= 10000 and section_count >= 5:
                quality_score = "🔶 FAIR (4/10)"
            
            print(f"   Quality Assessment: {quality_score}")
            
            # Show content structure
            print(f"\\n📄 A+ CONTENT STRUCTURE:")
            lines = aplus_content.split('\\n')
            for i, line in enumerate(lines[:20]):  # Show first 20 lines
                if line.strip():
                    print(f"   {i+1:2d}: {line[:100]}...")
            
            if len(lines) > 20:
                print(f"   ... ({len(lines)-20} more lines)")
            
            # Show keywords analysis
            keywords = getattr(result, 'keywords', '')
            amazon_keywords = getattr(result, 'amazon_keywords', '')
            
            if keywords:
                keyword_list = [k.strip() for k in keywords.split(',') if k.strip()]
                short_tail = [k for k in keyword_list if len(k.split()) <= 2]
                long_tail = [k for k in keyword_list if len(k.split()) > 2]
                
                print(f"\\n🔑 KEYWORDS ANALYSIS:")
                print(f"   Total: {len(keyword_list)} (Target: 75+)")
                print(f"   Short-tail: {len(short_tail)} (Target: 35-40)")
                print(f"   Long-tail: {len(long_tail)} (Target: 35-40)")
                print(f"   amazon_keywords field: {'✅' if amazon_keywords else '❌'}")
            
            # Overall assessment
            issues = []
            if len(aplus_content) < 25000:
                issues.append(f"Need {25000 - len(aplus_content):,} more A+ chars")
            if section_count < 8:
                issues.append(f"Need {8 - section_count} more sections")
            if len(keyword_list if keywords else []) < 75:
                issues.append(f"Need {75 - len(keyword_list if keywords else [])} more keywords")
            
            print(f"\\n🎯 FINAL ASSESSMENT:")
            if not issues:
                print("   🎉 PERFECT! All targets achieved for 10/10 quality!")
            else:
                print(f"   📈 PROGRESS: {len(issues)} remaining issues:")
                for i, issue in enumerate(issues, 1):
                    print(f"      {i}. {issue}")
            
            return len(aplus_content) >= 25000 and section_count >= 8
        
        else:
            print("❌ Failed to generate listing")
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
    success = test_enhanced_aplus_generation()
    if success:
        print("\\n✅ Enhanced A+ content generation successful!")
    else:
        print("\\n❌ Enhanced A+ content generation needs improvement")