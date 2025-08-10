#!/usr/bin/env python3
"""
Check if occasion was stored in the product
"""

import requests
import json

def check_product_occasion():
    """Check if the occasion field exists in product 275"""
    
    base_url = "http://localhost:8000/api"
    
    try:
        # Get the product we just created (ID 275)
        response = requests.get(
            f"{base_url}/core/products/275/",
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            product_data = response.json()
            
            print("Product Data Fields:")
            for key, value in product_data.items():
                print(f"  {key}: {value}")
            
            # Check specifically for occasion
            occasion = product_data.get('occasion', 'FIELD_NOT_FOUND')
            print(f"\nOccasion field: '{occasion}'")
            
            if occasion and occasion != 'FIELD_NOT_FOUND':
                print("SUCCESS: Occasion field is working")
                return True
            else:
                print("ISSUE: Occasion field not found or empty")
                return False
        else:
            print(f"Failed to get product: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    check_product_occasion()