import requests
import json

print("TESTING CLEAN ETSY ENDPOINT")
print("=" * 35)

# Test 1: Etsy product creation with auto-detection
print("1. TESTING AUTO-DETECTION:")
print("-" * 25)

etsy_data = {
    'name': 'Handmade Ceramic Coffee Mug with Artistic Glaze',
    'description': 'Beautiful handcrafted ceramic mug perfect for your morning coffee ritual. Each piece is uniquely made by hand with sustainable materials and artistic flair.',
    'brand_name': 'ArtisanCrafts',
    'price': 28.99,
    'categories': 'Home & Living, Kitchen & Dining, Drinkware',
    'features': 'Handcrafted ceramic\nEco-friendly glaze\nDishwasher safe\nUnique patterns\nMade to order',
    'occasion': 'self_care',
    # No brand_tone - let it auto-detect
}

try:
    response = requests.post(
        'http://localhost:8000/api/core/etsy/create/',
        json=etsy_data,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"Response Status: {response.status_code}")
    
    if response.status_code == 201:
        print("SUCCESS! Etsy endpoint works!")
        response_data = response.json()
        print(f"   Product ID: {response_data.get('id')}")
        print(f"   Auto-detected Brand Tone: {response_data.get('brand_tone')}")
        print(f"   Message: {response_data.get('message')}")
        
    else:
        print("Error:")
        try:
            error_data = response.json()
            print(f"   Error: {json.dumps(error_data, indent=2)}")
        except:
            print(f"   Raw response: {response.text}")
            
except Exception as e:
    print(f"Request failed: {e}")

# Test 2: Brand tones endpoint
print("\n2. TESTING BRAND TONES ENDPOINT:")
print("-" * 32)

try:
    response = requests.get('http://localhost:8000/api/core/etsy/brand-tones/')
    if response.status_code == 200:
        brand_tones = response.json()['brand_tones']
        print(f"SUCCESS! Retrieved {len(brand_tones)} brand tones:")
        for tone in brand_tones[:5]:  # Show first 5
            print(f"   - {tone['label']} ({tone['value']})")
        print("   ...")
    else:
        print(f"Failed: {response.status_code}")
except Exception as e:
    print(f"Failed: {e}")

# Test 3: Occasions endpoint
print("\n3. TESTING OCCASIONS ENDPOINT:")
print("-" * 28)

try:
    response = requests.get('http://localhost:8000/api/core/etsy/occasions/')
    if response.status_code == 200:
        occasions = response.json()['occasions']
        print(f"SUCCESS! Retrieved {len(occasions)} occasions:")
        for occasion in occasions[:5]:  # Show first 5
            print(f"   - {occasion['label']} ({occasion['value']})")
        print("   ...")
    else:
        print(f"Failed: {response.status_code}")
except Exception as e:
    print(f"Failed: {e}")

print("\n" + "=" * 35)
print("ETSY ENDPOINT TESTING COMPLETE")