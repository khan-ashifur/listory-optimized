import requests
import json
import urllib.parse

print("TESTING DIFFERENT HTTP REQUEST METHODS")
print("=" * 45)

api_data = {
    'name': 'HTTP Method Test',
    'description': 'Test different request formats',
    'brand_name': 'TestBrand',
    'target_platform': 'etsy',
    'marketplace': 'etsy',
    'price': 29.99,
    'brand_tone': 'handmade'
}

base_url = 'http://localhost:8000/api/core/products/'

# Test 1: JSON with different content types
print("\n1. TESTING DIFFERENT CONTENT TYPES:")
print("-" * 38)

content_types = [
    'application/json',
    'application/json; charset=utf-8',
    'text/json'
]

for ct in content_types:
    try:
        response = requests.post(
            base_url,
            json=api_data,
            headers={'Content-Type': ct}
        )
        print(f"   {ct}: {response.status_code}")
        if response.status_code != 201:
            try:
                error = response.json()
                print(f"      Error: {error.get('marketplace', 'Other error')}")
            except:
                print(f"      Raw: {response.text[:100]}")
    except Exception as e:
        print(f"   {ct}: Failed - {e}")

# Test 2: Form data instead of JSON
print("\n2. TESTING FORM DATA:")
print("-" * 20)

try:
    response = requests.post(
        base_url,
        data=api_data,  # Use data instead of json
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    print(f"   Form data: {response.status_code}")
    if response.status_code != 201:
        try:
            error = response.json()
            print(f"      Error: {error.get('marketplace', 'Other error')}")
        except:
            print(f"      Raw: {response.text[:100]}")
except Exception as e:
    print(f"   Form data: Failed - {e}")

# Test 3: Raw JSON string
print("\n3. TESTING RAW JSON STRING:")
print("-" * 30)

try:
    response = requests.post(
        base_url,
        data=json.dumps(api_data),
        headers={'Content-Type': 'application/json'}
    )
    print(f"   Raw JSON: {response.status_code}")
    if response.status_code != 201:
        try:
            error = response.json()
            print(f"      Error: {error.get('marketplace', 'Other error')}")
        except:
            print(f"      Raw: {response.text[:100]}")
except Exception as e:
    print(f"   Raw JSON: Failed - {e}")

print("\n" + "=" * 45)
print("HTTP METHOD TESTING COMPLETE")