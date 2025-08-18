#!/usr/bin/env python3
import sys
import os

# Add the backend path so we can import Django components
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory_backend.settings')

# Initialize Django
import django
django.setup()

from apps.listings.services import ListingGeneratorService
from apps.core.models import Product
import json

print("Creating test product...")

# Create a minimal test product
product = Product.objects.create(
    name="Test Headphones",
    description="Test description",
    brand_name="TestBrand",
    marketplace="tr",
    marketplace_language="tr",
    categories="electronics",
    price=40.00
)

print("Generating listing with AI...")

try:
    service = ListingGeneratorService()
    
    # Call the AI directly to see raw response
    response = service._call_openai_api(
        product=product,
        marketplace="tr", 
        marketplace_lang="tr"
    )
    
    print("RAW AI RESPONSE DEBUG:")
    print("="*60)
    
    if response:
        # Try to parse as JSON
        try:
            parsed = json.loads(response)
            
            # Check for aPlusContentPlan
            aplus_plan = parsed.get('aPlusContentPlan', {})
            print(f"aPlusContentPlan exists: {bool(aplus_plan)}")
            
            if aplus_plan:
                print("aPlusContentPlan keys:", list(aplus_plan.keys()))
                
                # Check for overallStrategy
                overall_strategy = aplus_plan.get('overallStrategy', '')
                print(f"overallStrategy exists: {bool(overall_strategy)}")
                if overall_strategy:
                    print(f"overallStrategy content: {overall_strategy}")
                else:
                    print("overallStrategy is missing or empty!")
            else:
                print("aPlusContentPlan is missing!")
                
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
            print("Raw response preview:", response[:500])
    else:
        print("No response from AI")
        
finally:
    # Clean up
    product.delete()
    print("Test complete - product deleted")