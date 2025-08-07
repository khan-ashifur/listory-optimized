#!/usr/bin/env python3
"""
Test to fetch the latest Walmart listing and check its data structure
"""

import requests
import json

def test_walmart_api():
    """Test the Walmart listing API"""
    
    base_url = "http://localhost:8000/api"
    
    try:
        # Get the latest listing (ID 343 from previous test)
        print("Fetching Walmart listing ID 343...")
        response = requests.get(
            f"{base_url}/listings/generated/343/",
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            listing_data = response.json()
            
            print("Walmart Listing Data Structure:")
            print("=" * 50)
            
            # Check platform
            platform = listing_data.get('platform', 'N/A')
            print(f"Platform: {platform}")
            
            # Check Walmart-specific fields
            walmart_fields = [
                'walmart_product_title',
                'walmart_description', 
                'walmart_key_features',
                'walmart_specifications',
                'walmart_gtin_upc',
                'walmart_manufacturer_part',
                'walmart_sku_id'
            ]
            
            print("\nWalmart-Specific Fields:")
            for field in walmart_fields:
                value = listing_data.get(field, '')
                if value and str(value).strip():
                    print(f"  {field}: {str(value)[:80]}...")
                else:
                    print(f"  {field}: [EMPTY]")
            
            # Check title length
            title = listing_data.get('walmart_product_title', '')
            if title:
                print(f"\nTitle Analysis:")
                print(f"  Length: {len(title)}/100 characters")
                print(f"  Compliant: {'Yes' if len(title) <= 100 else 'No'}")
            
            # Check specifications format
            specs = listing_data.get('walmart_specifications', '')
            if specs:
                try:
                    specs_data = json.loads(specs) if isinstance(specs, str) else specs
                    print(f"\nSpecifications:")
                    print(f"  Format: JSON (valid)")
                    print(f"  Keys: {list(specs_data.keys())[:5]}")
                except:
                    print(f"  Format: Text/Invalid JSON")
                    
            return True
        else:
            print(f"Failed to fetch listing: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Test failed: {e}")
        return False

if __name__ == "__main__":
    test_walmart_api()