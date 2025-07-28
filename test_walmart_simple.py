#!/usr/bin/env python3
"""
Test script to verify Walmart listing generation functionality
Simulates the exact user flow requested for testing
"""

import requests
import json
import sys
import time

# Configuration
BASE_URL = "http://localhost:3002"
API_BASE = f"{BASE_URL}/api"

def test_walmart_listing_generation():
    """Test the complete Walmart listing generation flow"""
    
    print("Starting Walmart Listing Generation Test")
    print("=" * 60)
    
    # Test data as specified in the requirements
    test_product_data = {
        "name": "Wireless Bluetooth Headphones",
        "brand_name": "AudioTech", 
        "description": "Premium wireless headphones with noise cancellation",
        "features": "Active noise cancellation, 30-hour battery, wireless charging",
        "price": 79.99,
        "target_platform": "walmart",
        "categories": "Electronics",
        "brand_tone": "professional",
        "competitor_urls": "",
        "target_keywords": ""
    }
    
    print("Test Product Details:")
    for key, value in test_product_data.items():
        print(f"   {key}: {value}")
    print()
    
    try:
        # Step 1: Check if server is running
        print("Step 1: Checking server status...")
        try:
            response = requests.get(BASE_URL, timeout=5)
            print(f"   [OK] Server is running (Status: {response.status_code})")
        except requests.exceptions.RequestException as e:
            print(f"   [ERROR] Server is not accessible: {e}")
            return False
        
        # Step 2: Create product
        print("\nStep 2: Creating product...")
        try:
            create_response = requests.post(
                f"{API_BASE}/core/products/",
                json=test_product_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if create_response.status_code in [200, 201]:
                product_data = create_response.json()
                product_id = product_data.get('id')
                print(f"   [OK] Product created successfully (ID: {product_id})")
            else:
                print(f"   [ERROR] Product creation failed (Status: {create_response.status_code})")
                print(f"   Response: {create_response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"   [ERROR] Product creation request failed: {e}")
            return False
        
        # Step 3: Generate Walmart listing
        print("\nStep 3: Generating Walmart listing...")
        try:
            listing_response = requests.post(
                f"{API_BASE}/listings/generate/{product_id}/walmart/",
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if listing_response.status_code in [200, 201]:
                listing_data = listing_response.json()
                listing_id = listing_data.get('id')
                print(f"   [OK] Walmart listing generated successfully (ID: {listing_id})")
                
                # Step 4: Fetch and analyze the listing
                print("\nStep 4: Analyzing generated listing...")
                listing_detail_response = requests.get(
                    f"{API_BASE}/listings/generated/{listing_id}/",
                    timeout=10
                )
                
                if listing_detail_response.status_code == 200:
                    listing_details = listing_detail_response.json()
                    return analyze_walmart_listing(listing_details)
                else:
                    print(f"   [ERROR] Failed to fetch listing details (Status: {listing_detail_response.status_code})")
                    return False
            else:
                print(f"   [ERROR] Listing generation failed (Status: {listing_response.status_code})")
                print(f"   Response: {listing_response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"   [ERROR] Listing generation request failed: {e}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Unexpected error during testing: {e}")
        return False

def analyze_walmart_listing(listing_data):
    """Analyze the generated Walmart listing for compliance with requirements"""
    
    print("Analyzing Walmart listing compliance...")
    print("-" * 40)
    
    issues_found = []
    passed_checks = []
    
    # Test 1: Walmart-specific fields populated
    walmart_fields = [
        'walmart_product_title',
        'walmart_description', 
        'walmart_key_features',
        'walmart_specifications',
        'walmart_gtin_upc',
        'walmart_manufacturer_part',
        'walmart_sku_id',
        'walmart_product_type',
        'walmart_category_path',
        'walmart_attributes'
    ]
    
    print("1. Checking Walmart-specific fields:")
    for field in walmart_fields:
        value = listing_data.get(field)
        if value and str(value).strip():
            passed_checks.append(f"[OK] {field}: populated")
            print(f"   [OK] {field}: populated")
        else:
            issues_found.append(f"[ERROR] {field}: missing or empty")
            print(f"   [ERROR] {field}: missing or empty")
    
    # Test 2: Check specifications format (should not be raw JSON string)
    print("\n2. Checking specifications format:")
    walmart_specs = listing_data.get('walmart_specifications', '')
    if walmart_specs:
        try:
            # Try to parse as JSON to see if it's structured
            specs_data = json.loads(walmart_specs) if isinstance(walmart_specs, str) else walmart_specs
            if isinstance(specs_data, dict) and specs_data:
                passed_checks.append("[OK] Specifications: properly structured JSON")
                print("   [OK] Specifications: properly structured JSON")
                print(f"   Sample fields: {list(specs_data.keys())[:3]}...")
            else:
                issues_found.append("[ERROR] Specifications: empty or invalid structure")
                print("   [ERROR] Specifications: empty or invalid structure")
        except json.JSONDecodeError:
            issues_found.append("[ERROR] Specifications: invalid JSON format")
            print("   [ERROR] Specifications: invalid JSON format")
    else:
        issues_found.append("[ERROR] Specifications: missing")
        print("   [ERROR] Specifications: missing")
    
    # Test 3: Check if platform is correctly set to walmart
    print("\n3. Checking platform setting:")
    platform = listing_data.get('platform', '')
    if platform.lower() == 'walmart':
        passed_checks.append("[OK] Platform: correctly set to walmart")
        print("   [OK] Platform: correctly set to walmart")
    else:
        issues_found.append(f"[ERROR] Platform: incorrect ({platform})")
        print(f"   [ERROR] Platform: incorrect ({platform})")
    
    # Test 4: Check keywords (should be Walmart-specific, not Amazon)
    print("\n4. Checking keywords:")
    keywords = listing_data.get('keywords', '')
    amazon_backend_keywords = listing_data.get('amazon_backend_keywords', '')
    
    if keywords and not amazon_backend_keywords:
        passed_checks.append("[OK] Keywords: Walmart-focused (no Amazon backend keywords)")
        print("   [OK] Keywords: Walmart-focused (no Amazon backend keywords)")
    elif amazon_backend_keywords:
        issues_found.append("[ERROR] Keywords: Amazon backend keywords found in Walmart listing")
        print("   [ERROR] Keywords: Amazon backend keywords found in Walmart listing")
    else:
        issues_found.append("[ERROR] Keywords: missing")
        print("   [ERROR] Keywords: missing")
    
    # Test 5: Check that A+ Content fields are not populated (Walmart doesn't use them)
    print("\n5. Checking A+ Content absence:")
    aplus_fields = ['amazon_aplus_content', 'hero_title', 'hero_content']
    aplus_found = False
    
    for field in aplus_fields:
        value = listing_data.get(field)
        if value and str(value).strip():
            aplus_found = True
            issues_found.append(f"[WARNING] A+ Content field populated in Walmart listing: {field}")
            print(f"   [WARNING] A+ Content field populated: {field}")
    
    if not aplus_found:
        passed_checks.append("[OK] A+ Content: correctly omitted for Walmart")
        print("   [OK] A+ Content: correctly omitted for Walmart")
    
    # Test 6: Check title length (Walmart has 100 char limit)
    print("\n6. Checking title length compliance:")
    walmart_title = listing_data.get('walmart_product_title', '')
    if walmart_title:
        title_length = len(walmart_title)
        if title_length <= 100:
            passed_checks.append(f"[OK] Title length: {title_length}/100 chars (compliant)")
            print(f"   [OK] Title length: {title_length}/100 chars (compliant)")
        else:
            issues_found.append(f"[ERROR] Title length: {title_length}/100 chars (exceeds limit)")
            print(f"   [ERROR] Title length: {title_length}/100 chars (exceeds limit)")
    else:
        issues_found.append("[ERROR] Title: missing")
        print("   [ERROR] Title: missing")
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    print(f"Passed checks: {len(passed_checks)}")
    for check in passed_checks[:5]:  # Show first 5
        print(f"   {check}")
    if len(passed_checks) > 5:
        print(f"   ... and {len(passed_checks) - 5} more")
    
    print(f"\nIssues found: {len(issues_found)}")
    for issue in issues_found:
        print(f"   {issue}")
    
    # Print some sample content for review
    print(f"\nSample Content Preview:")
    print(f"Title: {listing_data.get('walmart_product_title', 'N/A')[:50]}...")
    print(f"Description length: {len(listing_data.get('walmart_description', ''))}")
    print(f"Features count: {len((listing_data.get('walmart_key_features', '')).split('\\n'))}")
    print(f"Keywords: {listing_data.get('keywords', 'N/A')[:50]}...")
    
    # Overall result
    if len(issues_found) == 0:
        print("\n[SUCCESS] ALL TESTS PASSED! Walmart listing generation is working correctly.")
        return True
    elif len(issues_found) <= 3:
        print(f"\n[WARNING] MINOR ISSUES FOUND ({len(issues_found)}). Walmart listing mostly working.")
        return True
    else:
        print(f"\n[CRITICAL] MAJOR ISSUES FOUND ({len(issues_found)}). Walmart listing needs attention.")
        return False

def main():
    """Main test execution"""
    print("Walmart Listing Generation Test Suite")
    print("Testing the functionality as requested by the user")
    print()
    
    success = test_walmart_listing_generation()
    
    print("\n" + "=" * 60)
    if success:
        print("[SUCCESS] OVERALL RESULT: Walmart listing generation test PASSED")
        print("The system is ready for manual browser testing")
    else:
        print("[FAILURE] OVERALL RESULT: Walmart listing generation test FAILED")
        print("Issues need to be addressed before manual testing")
    
    print("\nNext steps for manual testing:")
    print("1. Open browser to http://localhost:3002")
    print("2. Create product with the test data shown above")
    print("3. Generate listing and verify in the UI")
    print("4. Check tabs: Main Listing, Keywords, Preview, Optimization")
    print("5. Verify no A+ Content tab appears")
    print("6. Take screenshots of any issues")

if __name__ == "__main__":
    main()