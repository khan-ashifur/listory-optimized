"""
Debug Turkey Marketplace Language Detection
"""
import os
import sys
import django

# Set up Django
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
os.chdir(backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product

def debug_turkey_marketplace_lang():
    """Debug Turkey marketplace language detection"""
    try:
        print("🔍 Debugging Turkey marketplace language...")
        
        # Get Turkey product
        product = Product.objects.filter(marketplace='tr').first()
        if not product:
            print("❌ No Turkey products found")
            return
        
        print(f"✅ Turkey Product: {product.name} (ID: {product.id})")
        print(f"   - marketplace: '{product.marketplace}'")
        
        # Check marketplace_language attribute
        marketplace_lang = getattr(product, 'marketplace_language', 'en')
        print(f"   - marketplace_language: '{marketplace_lang}'")
        print(f"   - Has marketplace_language attribute: {hasattr(product, 'marketplace_language')}")
        
        # Check what all fields the product has
        print(f"   - All product fields: {[field.name for field in product._meta.fields]}")
        
        # Test the condition used in services.py
        condition_1516 = marketplace_lang and marketplace_lang != 'en'
        print(f"   - Condition (marketplace_lang and marketplace_lang != 'en'): {condition_1516}")
        
        # Test Turkey marketplace condition
        marketplace = getattr(product, 'marketplace', 'com')
        condition_1520 = marketplace == 'tr'
        print(f"   - Turkey condition (marketplace == 'tr'): {condition_1520}")
        
        print(f"\n🎯 ISSUE ANALYSIS:")
        if not condition_1516:
            print(f"   ❌ Turkey enhancement won't be applied because marketplace_lang='{marketplace_lang}' (should be 'tr')")
            print(f"   🔧 Fix: Need to set marketplace_language='tr' for Turkey products")
        else:
            print(f"   ✅ Turkey enhancement should be applied")
            
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_turkey_marketplace_lang()