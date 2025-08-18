"""
Debug A+ content section extraction to see individual section lengths
"""

import os
import sys
import django

# Add the project path and configure Django
project_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

def debug_section_extraction():
    """Debug A+ content section extraction"""
    
    try:
        from apps.listings.services import ListingGeneratorService
        from apps.core.models import Product
        from django.contrib.auth.models import User
        import json

        print("🔍 DEBUGGING A+ SECTION EXTRACTION")
        print("=" * 50)
        
        user, _ = User.objects.get_or_create(
            username='debug_sections', 
            defaults={'email': 'test@test.com'}
        )
        
        product = Product.objects.create(
            user=user,
            name='プレミアムイヤホン',
            description='高品質テスト',
            brand_name='TestBrand',
            marketplace='jp',
            marketplace_language='ja',
            features='ノイズキャンセリング,バッテリー',
            price=12800,
            occasion='正月'
        )
        
        service = ListingGeneratorService()
        
        # Hook into the generation process to capture aPlusContentPlan
        original_generate = service._generate_amazon_listing
        
        def debug_generate(product, listing):
            result = original_generate(product, listing)
            
            # Access the raw result to check aPlusContentPlan
            if hasattr(service, '_last_result'):
                raw_result = service._last_result
            else:
                # Try to access the result from the listing generation
                print("⚠️ Cannot access raw result")
                return result
            
            return result
        
        service._generate_amazon_listing = debug_generate
        
        result = service.generate_listing(product.id, 'amazon')
        
        if result:
            aplus_content = getattr(result, 'amazon_aplus_content', '')
            
            print(f"📊 A+ CONTENT ANALYSIS:")
            print(f"   Total length: {len(aplus_content):,} characters")
            
            # Parse individual sections
            sections = aplus_content.split('<h3>')[1:]  # Skip first empty split
            
            print(f"   Number of sections found: {len(sections)}")
            print(f"   Expected sections: 8")
            
            total_content_chars = 0
            for i, section in enumerate(sections, 1):
                if '</h3>' in section:
                    title_end = section.find('</h3>')
                    title = section[:title_end]
                    content_part = section[title_end+5:]  # Skip </h3>
                    
                    # Extract just the content between <p> and </p>
                    if '<p>' in content_part and '</p>' in content_part:
                        p_start = content_part.find('<p>') + 3
                        p_end = content_part.find('</p>')
                        content = content_part[p_start:p_end]
                    else:
                        content = content_part[:100] + "..." if len(content_part) > 100 else content_part
                    
                    content_chars = len(content)
                    total_content_chars += content_chars
                    
                    print(f"   Section {i}: {title[:30]}... ({content_chars} chars)")
                    print(f"      Content preview: {content[:80]}...")
            
            print(f"\\n📈 CHARACTER ANALYSIS:")
            print(f"   Total content characters: {total_content_chars:,}")
            print(f"   Average per section: {total_content_chars // len(sections) if sections else 0:,}")
            print(f"   Target per section: 600-1400 characters")
            print(f"   Target total: 4,800-11,200 characters")
            
            quality_assessment = "❌ POOR (2/10)"
            if total_content_chars >= 8000 and len(sections) >= 8:
                quality_assessment = "✅ EXCELLENT (10/10)"
            elif total_content_chars >= 6000 and len(sections) >= 7:
                quality_assessment = "🟡 VERY GOOD (8/10)"
            elif total_content_chars >= 4000 and len(sections) >= 6:
                quality_assessment = "⚠️ GOOD (6/10)"
            
            print(f"   Quality: {quality_assessment}")
            
        else:
            print("❌ Failed to generate listing")
        
        return True
        
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
    debug_section_extraction()