import requests
import json

print("TESTING ETSY AUTO-DETECTION")
print("=" * 30)

etsy_data = {
    'name': 'Handmade Ceramic Coffee Mug',
    'description': 'Beautiful handcrafted ceramic mug made by hand with artistic flair',
    'brand_name': 'TestBrand',
    'target_platform': 'etsy',
    'price': 29.99,
    'categories': 'Home & Living',
    'features': 'Handcrafted ceramic\nArtisan made\nUnique patterns',
    # No brand_tone - let it auto-detect
}

try:
    response = requests.post(
        'http://localhost:8000/api/core/products/create_safe/',
        json=etsy_data,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"Response Status: {response.status_code}")
    
    if response.status_code == 201:
        response_data = response.json()
        print("SUCCESS! Etsy auto-detection works!")
        print(f"   Product ID: {response_data.get('id')}")
        print(f"   Name: {response_data.get('name')}")
        print(f"   Brand Tone: {response_data.get('brand_tone')}")
        print(f"   Platform: {response_data.get('target_platform')}")
        print(f"   Marketplace: {response_data.get('marketplace')}")
        
        if 'message' in response_data:
            print(f"   Message: {response_data['message']}")
            
    else:
        print("Error:")
        try:
            error_data = response.json()
            print(f"   Error: {json.dumps(error_data, indent=2)}")
        except:
            print(f"   Raw response: {response.text}")
            
except Exception as e:
    print(f"Request failed: {e}")

print("\n" + "=" * 30)
print("TEST COMPLETE")