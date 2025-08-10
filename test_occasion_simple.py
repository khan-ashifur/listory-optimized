#!/usr/bin/env python3
"""
Simple test to verify occasion field is working
"""

import requests
import json

def test_occasion_data():
    """Test that occasion data is properly stored"""
    
    base_url = "http://localhost:8000/api"
    
    # Test creating product with occasion
    product_data = {
        "name": "Christmas Gift Headphones",
        "brand_name": "HolidayAudio", 
        "description": "Perfect wireless headphones for Christmas gifts",
        "features": "Active noise cancellation\n30-hour battery\nComfortable design",
        "price": 79.99,
        "categories": "Electronics",
        "brand_tone": "professional",
        "occasion": "christmas",
        "target_platform": "amazon"
    }
    
    print("Testing Occasion Field Storage:")
    print(f"Test Product: {product_data['name']}")
    print(f"Test Occasion: {product_data['occasion']}")
    
    try:
        # Create product
        create_response = requests.post(
            f"{base_url}/core/products/",
            json=product_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if create_response.status_code in [200, 201]:
            result = create_response.json()
            product_id = result.get('id')
            stored_occasion = result.get('occasion', 'NOT_FOUND')
            
            print(f"Product Created: ID {product_id}")
            print(f"Occasion Stored: '{stored_occasion}'")
            
            if stored_occasion == product_data['occasion']:
                print("✅ PASS: Occasion field correctly stored and retrieved")
                return True
            else:
                print("❌ FAIL: Occasion field not matching")
                return False
        else:
            print(f"❌ FAIL: Product creation failed - {create_response.status_code}")
            print(create_response.text)
            return False
            
    except Exception as e:
        print(f"❌ FAIL: Test error - {e}")
        return False

if __name__ == "__main__":
    success = test_occasion_data()
    print(f"\nResult: {'SUCCESS' if success else 'FAILED'}")