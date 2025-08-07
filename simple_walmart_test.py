#!/usr/bin/env python3
"""
Simple test for Walmart listing generation
"""

import requests
import json
import sys

def test_walmart_generation():
    """Test Walmart listing generation via API"""
    
    base_url = "http://localhost:8000/api"
    
    # Test data
    product_data = {
        "name": "Wireless Bluetooth Headphones",
        "brand_name": "AudioTech", 
        "description": "Premium wireless headphones with noise cancellation",
        "features": "Active noise cancellation\n30-hour battery\nwireless charging",
        "price": 79.99,
        "target_platform": "walmart",
        "categories": "Electronics",
        "brand_tone": "professional"
    }
    
    print("Testing Walmart listing generation...")
    print(f"Product: {product_data['name']}")
    
    try:
        # Step 1: Create product
        print("\nCreating product...")
        create_response = requests.post(
            f"{base_url}/core/products/",
            json=product_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if create_response.status_code in [200, 201]:
            product_data = create_response.json()
            product_id = product_data.get('id')
            print(f"Product created: ID {product_id}")
        else:
            print(f"Product creation failed: {create_response.status_code}")
            print(create_response.text)
            return False
        
        # Step 2: Generate Walmart listing
        print("\nGenerating Walmart listing...")
        listing_response = requests.post(
            f"{base_url}/listings/generate/{product_id}/walmart/",
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        if listing_response.status_code in [200, 201]:
            listing_data = listing_response.json()
            listing_id = listing_data.get('id')
            print(f"Walmart listing generated: ID {listing_id}")
            
            # Check key fields
            walmart_fields = [
                'walmart_product_title',
                'walmart_description', 
                'walmart_key_features',
                'walmart_specifications'
            ]
            
            print("\nChecking Walmart fields:")
            for field in walmart_fields:
                value = listing_data.get(field, '')
                if value and str(value).strip():
                    print(f"  {field}: OK")
                else:
                    print(f"  {field}: MISSING")
            
            return True
        else:
            print(f"Listing generation failed: {listing_response.status_code}")
            print(listing_response.text)
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return False
    except Exception as e:
        print(f"Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_walmart_generation()
    if success:
        print("\nWalmart test PASSED")
        sys.exit(0)
    else:
        print("\nWalmart test FAILED")
        sys.exit(1)