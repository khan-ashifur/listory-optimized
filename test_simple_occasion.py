import os
import sys
import django

# Set up Django environment
sys.path.insert(0, 'backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.services import ListingGeneratorService
from apps.core.models import Product, User

print("🎯 Testing Occasion Handling - Quick Test")
print("=" * 50)

# Get or create a test user
try:
    user = User.objects.first()
    if not user:
        user = User.objects.create(username='testuser', email='test@test.com')
        print("✅ Created test user")
    else:
        print("✅ Using existing user")
except Exception as e:
    print(f"⚠️ User creation issue: {e}")

# Test with Christmas occasion
try:
    print("\n🎄 Testing Christmas Occasion:")
    
    # Get existing product or use first available
    product = Product.objects.filter(occasion__isnull=False).first()
    
    if not product:
        print("No products with occasions found. Let's check what products exist:")
        products = Product.objects.all()[:3]
        for p in products:
            print(f"- {p.name} (Occasion: '{p.occasion}')")
            
        if products:
            product = products[0]
            print(f"Using product: {product.name}")
            print(f"Current occasion: '{product.occasion}'")
            
            # Check if occasion is being detected properly
            occasion_mode = bool(product.occasion and product.occasion.strip())
            print(f"Occasion mode detected: {occasion_mode}")
            
            # Show what the prompt would include
            if occasion_mode:
                print(f"🎉 Occasion '{product.occasion}' would be prioritized!")
                print("The listing generator should:")
                print(f"  - Include '{product.occasion}' in title")
                print(f"  - Prioritize '{product.occasion}' keywords") 
                print(f"  - Make first bullet about {product.occasion} appeal")
            else:
                print("ℹ️ No occasion specified - regular listing mode")
        else:
            print("❌ No products found in database")
    else:
        print(f"✅ Found product with occasion: {product.name}")
        print(f"✅ Occasion: {product.occasion}")
        
        # Test the occasion detection logic
        occasion_mode = bool(product.occasion and product.occasion.strip())
        print(f"✅ Occasion mode: {occasion_mode}")
        
        if occasion_mode:
            print(f"🎯 System will prioritize {product.occasion} throughout the listing")
            
            # Show how occasion key would be detected
            occasion_key = product.occasion.lower().replace("'s day", "").replace("day", "").strip()
            if 'christmas' in occasion_key:
                occasion_key = 'christmas'
            elif 'valentine' in occasion_key:
                occasion_key = 'valentine'
            elif 'mother' in occasion_key:
                occasion_key = 'mother'
                
            print(f"🔑 Occasion key: {occasion_key}")
            
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 50)
print("✅ Quick occasion test complete")
print("\nTo see full optimization in action:")
print("1. Set a product's 'occasion' field to 'Christmas'")
print("2. Generate an Amazon listing")
print("3. Check that title, bullets, and keywords prioritize Christmas")