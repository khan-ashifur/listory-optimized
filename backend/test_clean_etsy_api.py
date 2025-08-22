import requests
import json

print("TESTING CLEAN ETSY API WITH NEW SERIALIZER")
print("=" * 45)

# Test Etsy product creation with auto-detection
etsy_data = {
    'name': 'Handmade Ceramic Coffee Mug',
    'description': 'Beautiful handcrafted ceramic mug perfect for your morning coffee ritual. Made with sustainable materials and artistic flair.',
    'brand_name': 'ArtisanCrafts',
    'target_platform': 'etsy',
    'marketplace': 'etsy',
    'price': 28.99,
    'categories': 'Home & Living, Kitchen & Dining, Drinkware',
    'features': 'Handcrafted ceramic\nEco-friendly glaze\nDishwasher safe\nUnique patterns\nMade to order',
    # Don't set brand_tone - let it auto-detect
}

try:
    response = requests.post(
        'http://localhost:8000/api/core/products/',
        json=etsy_data,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"Clean API Response: {response.status_code}")
    
    if response.status_code == 201:
        print("SUCCESS! Clean Etsy API works!")
        response_data = response.json()
        print(f"   Product ID: {response_data.get('id')}")
        print(f"   Product Name: {response_data.get('name')}")
        print(f"   Auto-detected Brand Tone: {response_data.get('brand_tone')}")
        print(f"   Platform: {response_data.get('target_platform')}")
        print(f"   Marketplace: {response_data.get('marketplace')}")
        
    else:
        print("API Error:")
        try:
            error_data = response.json()
            print(f"   Error: {json.dumps(error_data, indent=2)}")
        except:
            print(f"   Raw response: {response.text}")
            
except Exception as e:
    print(f"Request failed: {e}")

print("\n" + "=" * 45)
print("CLEAN API TEST COMPLETE")