#!/usr/bin/env python
"""
Simple test script to debug API issues
"""
import requests
import json

print("🔍 Testing Listory API...")
print("=" * 50)

# Test 1: Basic API test
try:
    print("\n1️⃣  Testing basic API connection...")
    response = requests.get('http://localhost:8000/api/core/test/')
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    if response.status_code != 200:
        print("❌ Basic API test failed!")
        exit(1)
        
except Exception as e:
    print(f"❌ Connection error: {e}")
    print("Make sure Django server is running on localhost:8000")
    exit(1)

# Test 2: OpenAI configuration
try:
    print("\n2️⃣  Testing OpenAI configuration...")
    response = requests.get('http://localhost:8000/api/listings/generated/test_openai/')
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
except Exception as e:
    print(f"❌ OpenAI test error: {e}")

# Test 3: Create product
test_product = {
    "name": "Test Gaming Chair",
    "description": "Ergonomic gaming chair with lumbar support",
    "brand_name": "TestBrand",
    "brand_tone": "professional", 
    "price": "99.99",
    "categories": "Furniture, Gaming",
    "features": "Ergonomic, Adjustable height, Lumbar support",
    "competitor_urls": "",
    "target_keywords": "gaming chair, ergonomic chair",
    "target_platform": "amazon"
}

try:
    print("\n3️⃣  Testing product creation...")
    response = requests.post(
        'http://localhost:8000/api/core/products/',
        json=test_product,
        headers={'Content-Type': 'application/json'}
    )
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 201:
        product_data = response.json()
        product_id = product_data['id']
        print(f"   ✅ Created product ID: {product_id}")
        
        # Test 4: Generate listing
        print("\n4️⃣  Testing listing generation...")
        listing_response = requests.post(
            f'http://localhost:8000/api/listings/generate/{product_id}/amazon/',
            headers={'Content-Type': 'application/json'}
        )
        print(f"   Status: {listing_response.status_code}")
        
        if listing_response.status_code == 201:
            listing_data = listing_response.json()
            print(f"   ✅ Generated listing ID: {listing_data['id']}")
            print(f"   Title: {listing_data['title'][:100]}...")
        else:
            print(f"   ❌ Listing error: {listing_response.text}")
    else:
        print(f"   ❌ Product creation error: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 50)
print("🔍 Test completed!")