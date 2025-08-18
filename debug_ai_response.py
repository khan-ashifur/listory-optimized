#!/usr/bin/env python3
import json
import re

# Simulate the AI response to check if overallStrategy is being returned
test_ai_response = """
{
  "productTitle": "TestBrand Test Headphones",
  "aPlusContentPlan": {
    "hero_section": {
      "title": "Premium Audio Experience",
      "content": "Experience superior sound quality with our professional headphones."
    },
    "features_section": {
      "title": "Advanced Features", 
      "content": "Discover cutting-edge audio technology."
    },
    "overallStrategy": "Our comprehensive A+ content strategy guides customers from initial interest to purchase decision through compelling hero presentation, detailed feature explanations, and trust-building elements that showcase product quality and brand reliability."
  }
}
"""

try:
    # Parse the JSON
    parsed_response = json.loads(test_ai_response)
    
    print("CHECKING AI RESPONSE STRUCTURE")
    print("="*50)
    
    # Check if aPlusContentPlan exists
    aplus_plan = parsed_response.get('aPlusContentPlan', {})
    print(f"aPlusContentPlan exists: {bool(aplus_plan)}")
    
    # Check if overallStrategy exists
    overall_strategy = aplus_plan.get('overallStrategy', '')
    print(f"overallStrategy exists: {bool(overall_strategy)}")
    print(f"overallStrategy content: {overall_strategy}")
    
    # Test the HTML generation logic
    fallback_text = 'Complete A+ content plan designed to guide customers from awareness to purchase'
    final_strategy = aplus_plan.get('overallStrategy', fallback_text)
    print(f"Final strategy text: {final_strategy}")
    
    # Test HTML template
    strategy_html = f"""
<div class="aplus-strategy-summary bg-gray-50 p-4 sm:p-6 rounded-lg mt-6 mx-2 sm:mx-0">
    <h3 class="text-lg sm:text-xl font-semibold text-gray-900 mb-3">Overall A+ Strategy</h3>
    <p class="text-gray-700 text-sm sm:text-base leading-relaxed">{final_strategy}</p>
</div>"""
    
    print("GENERATED STRATEGY HTML:")
    print(strategy_html)
    
except json.JSONDecodeError as e:
    print(f"JSON parsing error: {e}")
except Exception as e:
    print(f"Error: {e}")