#!/usr/bin/env python3
"""
Simple German Market Testing Script
Tests key brand tones and occasions for Amazon Germany
"""

import json
import requests
import time

class GermanMarketTester:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"
        self.glitches_found = []
        
        # Test product for German market
        self.test_product = {
            "name": "Premium Tragbarer Ventilator",
            "brand_name": "TestBrand",
            "price": "39.99",
            "description": "Hochqualitativer tragbarer Ventilator mit USB-Aufladung",
            "marketplace": "de",
            "marketplace_language": "de",
            "category": "Home & Garden"
        }
    
    def create_test_product(self):
        """Create test product"""
        try:
            response = requests.post(f"{self.base_url}/api/products/", json=self.test_product)
            if response.status_code == 201:
                product_id = response.json().get("id")
                print(f"Test product created: ID {product_id}")
                return product_id
            else:
                print(f"Failed to create product: {response.status_code}")
                return None
        except Exception as e:
            print(f"Product creation error: {e}")
            return None
    
    def test_german_listing(self, product_id, brand_tone=None, occasion=None):
        """Test German listing generation"""
        listing_data = {
            "product": product_id,
            "marketplace": "de", 
            "marketplace_language": "de",
            "platform": "amazon"
        }
        
        if brand_tone:
            listing_data["brand_tone"] = brand_tone
        if occasion:
            listing_data["occasion"] = occasion
            
        test_name = brand_tone or occasion or "basic"
        print(f"\nTesting: {test_name}")
        
        try:
            response = requests.post(f"{self.base_url}/api/listings/generate/", json=listing_data)
            
            if response.status_code == 200:
                result = response.json()
                self.analyze_result(test_name, result)
                return result
            else:
                print(f"Failed: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def analyze_result(self, test_name, result):
        """Analyze results for German market compliance"""
        print(f"Analyzing {test_name}...")
        
        listing = result.get('listing', {})
        title = listing.get('title', '')
        bullets = listing.get('bullet_points', [])
        description = listing.get('description', '')
        aplus = result.get('aplus_content_plan', {})
        
        print(f"Title: {title[:80]}...")
        print(f"Bullets count: {len(bullets)}")
        print(f"A+ sections: {len(aplus) if aplus else 0}")
        
        # Check German language
        full_content = title + " " + " ".join(bullets) + " " + description
        
        # Check for umlauts
        umlauts = ['ä', 'ö', 'ü', 'ß', 'Ä', 'Ö', 'Ü']
        umlaut_count = sum(full_content.count(char) for char in umlauts)
        print(f"German umlauts: {umlaut_count}")
        
        if umlaut_count == 0:
            self.glitches_found.append(f"{test_name}: No German umlauts found")
        
        # Check for English contamination
        english_words = ["the", "and", "with", "for", "quality", "professional"]
        english_found = [word for word in english_words if word.lower() in full_content.lower()]
        
        if english_found:
            self.glitches_found.append(f"{test_name}: English words found: {english_found}")
        
        # Check A+ structure
        if not aplus:
            self.glitches_found.append(f"{test_name}: No A+ content generated")
        else:
            expected_sections = ["section1_hero", "section2_features", "section3_trust", "section4_faqs"]
            missing = [s for s in expected_sections if s not in aplus]
            if missing:
                self.glitches_found.append(f"{test_name}: Missing A+ sections: {missing}")
        
        print(f"Analysis complete for {test_name}")
        return {
            "title": title,
            "bullet_count": len(bullets),
            "aplus_sections": len(aplus) if aplus else 0,
            "umlauts": umlaut_count,
            "english_contamination": len(english_found)
        }
    
    def run_tests(self):
        """Run key tests"""
        print("Starting German Market Testing...")
        
        # Create test product
        product_id = self.create_test_product()
        if not product_id:
            return
        
        # Test key brand tones
        brand_tones = ["professional", "casual", "luxury"]
        for tone in brand_tones:
            self.test_german_listing(product_id, brand_tone=tone)
            time.sleep(1)
        
        # Test key occasions
        occasions = ["Christmas", "Mother's Day", "Valentine's Day"]
        for occasion in occasions:
            self.test_german_listing(product_id, occasion=occasion)
            time.sleep(1)
        
        # Print results
        print("\n" + "="*50)
        print("GERMAN MARKET TEST RESULTS")
        print("="*50)
        
        if self.glitches_found:
            print(f"\nGLITCHES FOUND ({len(self.glitches_found)}):")
            for i, glitch in enumerate(self.glitches_found, 1):
                print(f"{i}. {glitch}")
        else:
            print("\nNo critical glitches found!")
        
        print(f"\nTest completed: {len(self.glitches_found)} issues identified")

if __name__ == "__main__":
    tester = GermanMarketTester()
    tester.run_tests()