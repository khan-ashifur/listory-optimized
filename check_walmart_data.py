#!/usr/bin/env python3
"""
Check complete Walmart listing data
"""

import requests
import json

def check_walmart_data():
    """Check the complete Walmart listing data"""
    
    base_url = "http://localhost:8000/api"
    
    try:
        response = requests.get(
            f"{base_url}/listings/generated/343/",
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            listing_data = response.json()
            
            print("COMPLETE WALMART LISTING DATA:")
            print("=" * 60)
            
            # Key fields for preview
            key_fields = [
                'platform',
                'title',
                'walmart_product_title',
                'walmart_description',
                'walmart_key_features',
                'walmart_specifications',
                'product'
            ]
            
            for field in key_fields:
                value = listing_data.get(field, 'N/A')
                print(f"\n{field.upper()}:")
                if isinstance(value, dict):
                    print(json.dumps(value, indent=2)[:500] + "...")
                elif isinstance(value, str) and len(value) > 200:
                    print(f"  {value[:200]}...")
                else:
                    print(f"  {value}")
            
            return True
        else:
            print(f"Failed to fetch listing: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Check failed: {e}")
        return False

if __name__ == "__main__":
    check_walmart_data()