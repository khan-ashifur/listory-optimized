"""
Debug keyword mapping issue - keywords vs amazon_keywords field
"""

import os
import sys
import django

# Add the project path and configure Django
project_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

def debug_keyword_mapping():
    """Debug why keywords aren't showing in amazon_keywords field"""
    
    try:
        from apps.listings.services import ListingGeneratorService
        from apps.core.models import Product
        from django.contrib.auth.models import User
        from apps.listings.models import GeneratedListing

        print("🔍 DEBUGGING KEYWORD MAPPING ISSUE...")
        print("=" * 60)
        
        # Check what fields exist in the database model
        print("📊 CHECKING DATABASE MODEL FIELDS:")
        listing_fields = [f.name for f in GeneratedListing._meta.fields]
        print(f"   Total fields: {len(listing_fields)}")
        
        keyword_fields = [f for f in listing_fields if 'keyword' in f.lower()]
        print(f"   Keyword-related fields: {keyword_fields}")
        
        # Check if amazon_keywords field exists
        has_amazon_keywords = 'amazon_keywords' in listing_fields
        print(f"   Has amazon_keywords field: {'✅' if has_amazon_keywords else '❌'}")
        
        if not has_amazon_keywords:
            print("   🚨 CRITICAL: amazon_keywords field MISSING from database!")
            print("   📝 Available keyword fields:")
            for field in keyword_fields:
                print(f"      - {field}")
        
        # Test actual keyword generation
        print(f"\n🧪 TESTING KEYWORD GENERATION:")
        user, _ = User.objects.get_or_create(username='debug_keywords', defaults={'email': 'test@debug.com'})
        product = Product.objects.create(
            user=user,
            name='Test Product Keywords',
            description='Testing keyword mapping',
            brand_name='TestBrand',
            brand_tone='professional',
            target_platform='amazon',
            marketplace='de',
            marketplace_language='de',
            price=99,
            categories='Electronics',
            features='Test features'
        )
        
        service = ListingGeneratorService()
        result = service.generate_listing(product.id, 'amazon')
        
        if result:
            print("✅ Listing generated successfully!")
            
            # Check what keyword data is actually saved
            print(f"\n📋 KEYWORD DATA IN DATABASE:")
            print(f"   keywords field: '{getattr(result, 'keywords', 'NOT FOUND')}' ({len(getattr(result, 'keywords', '')) if getattr(result, 'keywords', '') else 0} chars)")
            print(f"   amazon_backend_keywords: '{getattr(result, 'amazon_backend_keywords', 'NOT FOUND')}' ({len(getattr(result, 'amazon_backend_keywords', '')) if getattr(result, 'amazon_backend_keywords', '') else 0} chars)")
            
            # Try to access amazon_keywords field
            try:
                amazon_keywords = getattr(result, 'amazon_keywords', None)
                print(f"   amazon_keywords field: '{amazon_keywords}' ({len(amazon_keywords) if amazon_keywords else 0} chars)")
            except AttributeError:
                print(f"   amazon_keywords field: ❌ ATTRIBUTE ERROR - Field doesn't exist!")
            
            # Count keywords in the keywords field
            if hasattr(result, 'keywords') and result.keywords:
                keyword_list = [k.strip() for k in result.keywords.split(',') if k.strip()]
                print(f"\n📊 KEYWORD ANALYSIS:")
                print(f"   Total keywords in 'keywords' field: {len(keyword_list)}")
                print(f"   First 5 keywords: {keyword_list[:5]}")
                
                # Analyze keyword types
                short_tail = [k for k in keyword_list if len(k.split()) <= 2]
                long_tail = [k for k in keyword_list if len(k.split()) > 2]
                
                print(f"   Short-tail keywords: {len(short_tail)}")
                print(f"   Long-tail keywords: {len(long_tail)}")
                
                print(f"\n🎯 SOLUTION NEEDED:")
                print(f"   The frontend expects 'amazon_keywords' field but it doesn't exist!")
                print(f"   Keywords are correctly saved to 'keywords' field: {len(keyword_list)} total")
                print(f"   Need to either:")
                print(f"     1. Add amazon_keywords field to database model")
                print(f"     2. Update frontend to use 'keywords' field")
                print(f"     3. Copy keywords to amazon_keywords during save")
            
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
    debug_keyword_mapping()