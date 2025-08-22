import requests
import json

print("TESTING AUTO-DETECTION LOGIC")
print("=" * 30)

# Test exact data that should trigger auto-detection
test_data = {
    'name': 'Handmade Ceramic Coffee Mug',
    'description': 'Beautiful handcrafted ceramic mug made by hand with artistic flair',
    'brand_name': 'TestBrand',
    'target_platform': 'etsy',
    'price': 29.99,
    'categories': 'Home & Living',
    'features': 'Handcrafted ceramic\nArtisan made\nUnique patterns',
    # Explicitly test different combinations
}

# Test 1: No brand_tone (should auto-detect)
print("TEST 1: No brand_tone provided")
print("-" * 30)
response1 = requests.post(
    'http://localhost:8000/api/core/products/create_safe/',
    json=test_data,
    headers={'Content-Type': 'application/json'}
)

if response1.status_code == 201:
    data1 = response1.json()
    print(f"  Brand Tone: '{data1.get('brand_tone')}'")
    print(f"  Marketplace: '{data1.get('marketplace')}'")
    print(f"  Message: {data1.get('message', 'No message')}")
else:
    print(f"  Failed: {response1.status_code}")
    print(f"  Error: {response1.text}")

# Test 2: Empty brand_tone (should auto-detect)
print("\nTEST 2: Empty brand_tone provided")
print("-" * 35)
test_data_empty = test_data.copy()
test_data_empty['brand_tone'] = ''

response2 = requests.post(
    'http://localhost:8000/api/core/products/create_safe/',
    json=test_data_empty,
    headers={'Content-Type': 'application/json'}
)

if response2.status_code == 201:
    data2 = response2.json()
    print(f"  Brand Tone: '{data2.get('brand_tone')}'")
    print(f"  Marketplace: '{data2.get('marketplace')}'")
    print(f"  Message: {data2.get('message', 'No message')}")
else:
    print(f"  Failed: {response2.status_code}")
    print(f"  Error: {response2.text}")

# Test 3: Manual brand_tone (should NOT auto-detect)
print("\nTEST 3: Manual brand_tone provided")
print("-" * 35)
test_data_manual = test_data.copy()
test_data_manual['brand_tone'] = 'vintage_charm'

response3 = requests.post(
    'http://localhost:8000/api/core/products/create_safe/',
    json=test_data_manual,
    headers={'Content-Type': 'application/json'}
)

if response3.status_code == 201:
    data3 = response3.json()
    print(f"  Brand Tone: '{data3.get('brand_tone')}'")
    print(f"  Marketplace: '{data3.get('marketplace')}'")
    print(f"  Message: {data3.get('message', 'No message')}")
else:
    print(f"  Failed: {response3.status_code}")
    print(f"  Error: {response3.text}")

print("\n" + "=" * 30)
print("LOGIC DEBUG COMPLETE")