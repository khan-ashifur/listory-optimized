import requests
import json

print("TESTING ETSY API AFTER SERIALIZER FIX")
print("=" * 45)

# Test Etsy marketplace API call
api_data = {
    'name': 'Fixed Etsy Product',
    'description': 'Test after serializer fix',
    'brand_name': 'TestBrand',
    'target_platform': 'etsy',
    'marketplace': 'etsy',
    'price': 29.99,
    'brand_tone': 'handmade'
}

try:
    response = requests.post(
        'http://localhost:8000/api/core/products/',
        json=api_data,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"API Response Status: {response.status_code}")
    
    if response.status_code == 201:
        print("SUCCESS! Etsy product created successfully!")
        response_data = response.json()
        print(f"   Product ID: {response_data.get('id')}")
        print(f"   Product Name: {response_data.get('name')}")
        print(f"   Marketplace: etsy")
        print(f"   Platform: etsy")
        
    else:
        print("STILL FAILING!")
        try:
            error_data = response.json()
            print(f"   Error: {json.dumps(error_data, indent=2)}")
        except:
            print(f"   Raw response: {response.text}")
            
except Exception as e:
    print(f"Request failed: {e}")

print("\n" + "=" * 45)
print("TEST COMPLETE")