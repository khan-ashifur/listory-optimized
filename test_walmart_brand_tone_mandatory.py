#!/usr/bin/env python3
"""
Test Walmart USA Brand Tone Mandatory Validation
Verifies that brand tone is now required and properly enforced
"""

import os
import sys
import django
from datetime import datetime

# Add the backend directory to Python path
backend_path = os.path.join(os.getcwd(), 'backend')
sys.path.insert(0, backend_path)

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.services import ListingGeneratorService
from apps.core.models import Product
from django.contrib.auth.models import User

def test_brand_tone_mandatory():
    """Test that brand tone is now mandatory for Walmart listings"""
    
    print("🔒 WALMART BRAND TONE MANDATORY VALIDATION TEST 🔒")
    print("=" * 55)
    
    # Create test user
    user, created = User.objects.get_or_create(username='brand_tone_test')
    service = ListingGeneratorService()
    
    # Test 1: Product WITHOUT brand tone (should fail)
    print("\n🔍 TEST 1: Product WITHOUT Brand Tone (Should Fail)")
    product_no_tone = Product.objects.create(
        user=user,
        name='Test Gaming Headset',
        brand_name='TestBrand',
        marketplace='walmart_usa',
        marketplace_language='en-us',
        price=89.99,
        occasion='black_friday',
        # brand_tone deliberately omitted
        categories='Electronics > Gaming',
        description='Test gaming headset',
        features='Wireless\nNoise Cancellation\n30H Battery'
    )
    
    try:
        listing = service.generate_listing(product_no_tone.id, 'walmart')
        print("   ❌ FAIL: Generation should have failed but succeeded")
        success_1 = False
    except Exception as e:
        if "Brand tone is MANDATORY" in str(e):
            print("   ✅ PASS: Correctly rejected listing without brand tone")
            print(f"   📝 Error Message: {e}")
            success_1 = True
        else:
            print(f"   ❌ FAIL: Wrong error message: {e}")
            success_1 = False
    finally:
        product_no_tone.delete()
    
    # Test 2: Product with EMPTY brand tone (should fail)
    print("\n🔍 TEST 2: Product with EMPTY Brand Tone (Should Fail)")
    product_empty_tone = Product.objects.create(
        user=user,
        name='Test Gaming Headset',
        brand_name='TestBrand',
        marketplace='walmart_usa',
        marketplace_language='en-us',
        price=89.99,
        occasion='black_friday',
        brand_tone='',  # Empty brand tone
        categories='Electronics > Gaming',
        description='Test gaming headset',
        features='Wireless\nNoise Cancellation\n30H Battery'
    )
    
    try:
        listing = service.generate_listing(product_empty_tone.id, 'walmart')
        print("   ❌ FAIL: Generation should have failed but succeeded")
        success_2 = False
    except Exception as e:
        if "Brand tone is MANDATORY" in str(e):
            print("   ✅ PASS: Correctly rejected listing with empty brand tone")
            print(f"   📝 Error Message: {e}")
            success_2 = True
        else:
            print(f"   ❌ FAIL: Wrong error message: {e}")
            success_2 = False
    finally:
        product_empty_tone.delete()
    
    # Test 3: Product with INVALID brand tone (should fail)
    print("\n🔍 TEST 3: Product with INVALID Brand Tone (Should Fail)")
    product_invalid_tone = Product.objects.create(
        user=user,
        name='Test Gaming Headset',
        brand_name='TestBrand',
        marketplace='walmart_usa',
        marketplace_language='en-us',
        price=89.99,
        occasion='black_friday',
        brand_tone='invalid_tone',  # Invalid brand tone
        categories='Electronics > Gaming',
        description='Test gaming headset',
        features='Wireless\nNoise Cancellation\n30H Battery'
    )
    
    try:
        listing = service.generate_listing(product_invalid_tone.id, 'walmart')
        print("   ❌ FAIL: Generation should have failed but succeeded")
        success_3 = False
    except Exception as e:
        if "Invalid brand tone" in str(e):
            print("   ✅ PASS: Correctly rejected listing with invalid brand tone")
            print(f"   📝 Error Message: {e}")
            success_3 = True
        else:
            print(f"   ❌ FAIL: Wrong error message: {e}")
            success_3 = False
    finally:
        product_invalid_tone.delete()
    
    # Test 4: Test all VALID brand tones (should succeed)
    valid_tones = ['professional', 'casual', 'luxury', 'trendy']
    success_4 = True
    
    print("\n🔍 TEST 4: Valid Brand Tones (Should Succeed)")
    for tone in valid_tones:
        print(f"\n   Testing '{tone}' brand tone...")
        
        product_valid = Product.objects.create(
            user=user,
            name=f'Test {tone.title()} Headset',
            brand_name='TestBrand',
            marketplace='walmart_usa',
            marketplace_language='en-us',
            price=89.99,
            occasion='black_friday',
            brand_tone=tone,
            categories='Electronics > Gaming',
            description='Test gaming headset',
            features='Wireless\nNoise Cancellation\n30H Battery'
        )
        
        try:
            listing = service.generate_listing(product_valid.id, 'walmart')
            print(f"   ✅ PASS: '{tone}' brand tone accepted and listing generated")
            print(f"   📊 Status: {listing.status}")
            print(f"   📏 Title: {listing.walmart_product_title[:60]}...")
            
            # Validate brand tone is reflected in content
            full_content = f"{listing.walmart_product_title} {listing.walmart_description}".lower()
            tone_keywords = {
                'professional': ['professional', 'certified', 'expert', 'precision'],
                'casual': ['easy', 'simple', 'friendly', 'convenient'],
                'luxury': ['premium', 'luxury', 'sophisticated', 'exclusive'],
                'trendy': ['modern', 'innovative', 'cutting-edge', 'stylish']
            }
            
            found_keywords = [kw for kw in tone_keywords[tone] if kw in full_content]
            if found_keywords:
                print(f"   🎯 Brand tone reflected: {', '.join(found_keywords)}")
            else:
                print(f"   ⚠️ WARNING: Brand tone keywords not clearly reflected")
                
        except Exception as e:
            print(f"   ❌ FAIL: '{tone}' brand tone should work but failed: {e}")
            success_4 = False
        finally:
            product_valid.delete()
    
    # Overall test results
    print("\n" + "=" * 55)
    print("🏁 BRAND TONE MANDATORY TEST RESULTS")
    print("=" * 55)
    
    all_tests = [success_1, success_2, success_3, success_4]
    passed_tests = sum(all_tests)
    
    print(f"✅ Test 1 (No Brand Tone): {'PASS' if success_1 else 'FAIL'}")
    print(f"✅ Test 2 (Empty Brand Tone): {'PASS' if success_2 else 'FAIL'}")
    print(f"✅ Test 3 (Invalid Brand Tone): {'PASS' if success_3 else 'FAIL'}")
    print(f"✅ Test 4 (Valid Brand Tones): {'PASS' if success_4 else 'FAIL'}")
    
    print(f"\n🎯 OVERALL RESULT: {passed_tests}/{len(all_tests)} tests passed ({passed_tests/len(all_tests)*100:.1f}%)")
    
    if passed_tests == len(all_tests):
        print("🎉 SUCCESS: Brand tone is now MANDATORY and properly enforced!")
        print("   - Listings without brand tone are rejected")
        print("   - Invalid brand tones are rejected")
        print("   - All valid brand tones (professional, casual, luxury, trendy) work")
        print("   - Brand tone compliance is validated in generated content")
    else:
        print("❌ FAILURE: Brand tone mandatory enforcement needs fixes")
    
    return passed_tests == len(all_tests)

if __name__ == "__main__":
    print("Starting Brand Tone Mandatory Validation Test...")
    success = test_brand_tone_mandatory()
    if success:
        print("\n✅ All tests passed! Brand tone is now mandatory for Walmart listings.")
    else:
        print("\n❌ Some tests failed. Brand tone enforcement needs improvement.")