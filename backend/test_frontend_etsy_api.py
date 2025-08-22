import requests
import json

print("TESTING FRONTEND ETSY API CALL")
print("=" * 35)

# Simulate exactly what the frontend sends
frontend_data = {
    'name': 'Handmade Ceramic Mug',
    'description': 'Beautiful handcrafted ceramic mug perfect for your morning coffee',
    'brand_name': 'ArtisanCrafts',
    'target_platform': 'etsy',
    'marketplace': 'etsy',
    'marketplace_language': 'en',
    'price': 24.99,
    'brand_tone': 'handmade',
    'categories': 'Home & Living, Kitchen & Dining, Drinkware',
    'features': 'Hand-thrown ceramic\nGlazing options\nDishwasher safe\nUnique patterns\nGift ready',
    'occasion': 'christmas'
}

try:
    response = requests.post(
        'http://localhost:8000/api/core/products/create_safe/',
        json=frontend_data,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"Frontend API Response: {response.status_code}")
    
    if response.status_code == 201:
        print("SUCCESS! Frontend Etsy product creation works!")
        response_data = response.json()
        print(f"   Product ID: {response_data.get('id')}")
        print(f"   Product Name: {response_data.get('name')}")
        print(f"   Brand Name: {response_data.get('brand_name')}")
        print(f"   Platform: {response_data.get('target_platform')}")
        print()
        print("Frontend can now create Etsy products successfully!")
        print("Next step: Navigate to http://localhost:3002 and test creating an Etsy product")
        
    else:
        print("Frontend API still failing:")
        try:
            error_data = response.json()
            print(f"   Error: {json.dumps(error_data, indent=2)}")
        except:
            print(f"   Raw response: {response.text}")
            
except Exception as e:
    print(f"Request failed: {e}")

print("\n" + "=" * 35)
print("FRONTEND API TEST COMPLETE")