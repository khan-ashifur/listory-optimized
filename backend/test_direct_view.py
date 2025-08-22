import requests
import json

print("TESTING DIRECT VIEW CREATION")
print("=" * 35)

# Test using the safe creation endpoint that bypasses DRF
api_data = {
    'name': 'Direct View Test',
    'description': 'Test bypassing DRF serializer',
    'brand_name': 'TestBrand',
    'target_platform': 'etsy',
    'marketplace': 'etsy',
    'price': 29.99,
    'brand_tone': 'handmade'
}

try:
    response = requests.post(
        'http://localhost:8000/api/core/products/create_safe/',
        json=api_data,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"Direct view response: {response.status_code}")
    
    if response.status_code == 201:
        print("SUCCESS! Direct view creation worked!")
        response_data = response.json()
        print(f"   Product ID: {response_data.get('id')}")
        print(f"   Product Name: {response_data.get('name')}")
        
    else:
        print("Direct view also failed:")
        try:
            error_data = response.json()
            print(f"   Error: {json.dumps(error_data, indent=2)}")
        except:
            print(f"   Raw response: {response.text}")
            
except Exception as e:
    print(f"Request failed: {e}")

print("\n" + "=" * 35)
print("DIRECT VIEW TEST COMPLETE")