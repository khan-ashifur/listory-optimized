"""
Quick test to verify amazon_keywords field is working
"""

import os
import sys
import django

# Add the project path and configure Django
project_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

def quick_keyword_test():
    """Quick test that amazon_keywords field exists and works"""
    
    try:
        from apps.listings.models import GeneratedListing
        from apps.core.models import Product
        from django.contrib.auth.models import User

        print("🚀 QUICK AMAZON_KEYWORDS FIELD TEST...")
        print("=" * 50)
        
        # Check if field exists in model
        model_fields = [f.name for f in GeneratedListing._meta.fields]
        has_amazon_keywords = 'amazon_keywords' in model_fields
        
        print(f"📊 Model Fields Check:")
        print(f"   amazon_keywords field exists: {'✅' if has_amazon_keywords else '❌'}")
        
        if has_amazon_keywords:
            # Create a simple test record
            user, _ = User.objects.get_or_create(username='quick_test', defaults={'email': 'test@test.com'})
            product = Product.objects.create(
                user=user,
                name='Quick Test',
                description='Quick test',
                brand_name='TestBrand'
            )
            
            listing = GeneratedListing.objects.create(
                product=product,
                platform='amazon',
                keywords='test, quick, keywords',
                amazon_keywords='test, quick, keywords'  # This should work now
            )
            
            print(f"✅ Successfully created listing with amazon_keywords!")
            print(f"   keywords: '{listing.keywords}'")
            print(f"   amazon_keywords: '{listing.amazon_keywords}'")
            print(f"   Fields match: {'✅' if listing.keywords == listing.amazon_keywords else '❌'}")
            
            # Cleanup
            listing.delete()
            product.delete()
            
            return True
        else:
            print("❌ amazon_keywords field missing from model!")
            return False
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    success = quick_keyword_test()
    if success:
        print("🎉 AMAZON_KEYWORDS FIELD WORKING!")
    else:
        print("🔧 STILL NEEDS FIXING")