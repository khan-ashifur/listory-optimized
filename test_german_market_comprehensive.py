#!/usr/bin/env python3
"""
Comprehensive German Market Testing Script
Tests all brand tones and occasions for Amazon Germany marketplace
Identifies glitches and structural differences in A+ content
"""

import json
import requests
import time
import os
import sys
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class GermanMarketTester:
    """Comprehensive tester for German marketplace listings"""
    
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"
        self.test_results = {}
        self.glitches_found = []
        
        # Test configurations
        self.brand_tones = ["professional", "casual", "luxury", "playful", "minimal", "bold"]
        self.occasions = [
            "Christmas", "Valentine's Day", "Mother's Day", "Father's Day", 
            "Easter", "Birthday", "Wedding", "Anniversary"
        ]
        
        # Test product data for German market
        self.test_product = {
            "name": "Premium Tragbarer Ventilator",
            "brand_name": "TestBrand",
            "price": "€39.99",
            "description": "Hochqualitativer tragbarer Ventilator mit USB-Aufladung",
            "marketplace": "de",
            "marketplace_language": "de",
            "category": "Home & Garden"
        }
    
    def setup_test_product(self):
        """Create or update test product for German market"""
        product_data = self.test_product.copy()
        
        try:
            # Create test product
            response = requests.post(f"{self.base_url}/api/products/", json=product_data)
            if response.status_code == 201:
                product_id = response.json().get("id")
                print(f"✅ Test product created: ID {product_id}")
                return product_id
            else:
                print(f"❌ Failed to create product: {response.text}")
                return None
        except Exception as e:
            print(f"❌ Product setup error: {e}")
            return None
    
    def test_brand_tone(self, product_id, brand_tone):
        """Test specific brand tone for German market"""
        print(f"\n🎨 Testing Brand Tone: {brand_tone.upper()} for Germany")
        
        listing_data = {
            "product": product_id,
            "marketplace": "de",
            "marketplace_language": "de",
            "brand_tone": brand_tone,
            "platform": "amazon"
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/listings/generate/", json=listing_data)
            
            if response.status_code == 200:
                result = response.json()
                self.analyze_german_brand_tone_result(brand_tone, result)
                return result
            else:
                print(f"❌ Brand tone {brand_tone} failed: {response.text}")
                self.glitches_found.append(f"Brand tone {brand_tone} generation failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Brand tone {brand_tone} error: {e}")
            self.glitches_found.append(f"Brand tone {brand_tone} exception: {str(e)}")
            return None
    
    def test_occasion(self, product_id, occasion):
        """Test specific occasion for German market"""
        print(f"\n🎁 Testing Occasion: {occasion.upper()} for Germany")
        
        listing_data = {
            "product": product_id,
            "marketplace": "de",
            "marketplace_language": "de",
            "occasion": occasion,
            "brand_tone": "professional",  # Use professional tone for occasion testing
            "platform": "amazon"
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/listings/generate/", json=listing_data)
            
            if response.status_code == 200:
                result = response.json()
                self.analyze_german_occasion_result(occasion, result)
                return result
            else:
                print(f"❌ Occasion {occasion} failed: {response.text}")
                self.glitches_found.append(f"Occasion {occasion} generation failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Occasion {occasion} error: {e}")
            self.glitches_found.append(f"Occasion {occasion} exception: {str(e)}")
            return None
    
    def analyze_german_brand_tone_result(self, brand_tone, result):
        """Analyze German brand tone result for glitches"""
        print(f"📊 Analyzing {brand_tone} results for Germany...")
        
        # Check basic structure
        listing = result.get('listing', {})
        title = listing.get('title', '')
        bullets = listing.get('bullet_points', [])
        description = listing.get('description', '')
        aplus_content = result.get('aplus_content_plan', {})
        
        # German language validation
        self.check_german_language_quality(brand_tone, title, bullets, description, aplus_content)
        
        # Brand tone validation
        self.check_brand_tone_application(brand_tone, title, bullets, description)
        
        # A+ content structure validation
        self.check_aplus_structure(brand_tone, aplus_content, "brand_tone")
        
        # Store results
        self.test_results[f"brand_tone_{brand_tone}"] = {
            "title": title,
            "bullets": bullets,
            "description": description[:200] + "..." if len(description) > 200 else description,
            "aplus_sections": list(aplus_content.keys()) if aplus_content else [],
            "german_umlauts_found": self.count_umlauts(title + " ".join(bullets) + description),
            "brand_tone_words_found": self.count_brand_tone_words(brand_tone, title + " ".join(bullets) + description)
        }
    
    def analyze_german_occasion_result(self, occasion, result):
        """Analyze German occasion result for glitches"""
        print(f"📊 Analyzing {occasion} results for Germany...")
        
        # Check basic structure
        listing = result.get('listing', {})
        title = listing.get('title', '')
        bullets = listing.get('bullet_points', [])
        description = listing.get('description', '')
        aplus_content = result.get('aplus_content_plan', {})
        
        # German language validation
        self.check_german_language_quality(occasion, title, bullets, description, aplus_content)
        
        # Occasion validation
        self.check_occasion_application(occasion, title, bullets, description)
        
        # A+ content structure validation
        self.check_aplus_structure(occasion, aplus_content, "occasion")
        
        # Store results
        self.test_results[f"occasion_{occasion}"] = {
            "title": title,
            "bullets": bullets,
            "description": description[:200] + "..." if len(description) > 200 else description,
            "aplus_sections": list(aplus_content.keys()) if aplus_content else [],
            "german_umlauts_found": self.count_umlauts(title + " ".join(bullets) + description),
            "occasion_references": self.count_occasion_references(occasion, title + " ".join(bullets) + description)
        }
    
    def check_german_language_quality(self, test_type, title, bullets, description, aplus_content):
        """Check German language quality and detect issues"""
        print(f"  🇩🇪 Checking German language quality for {test_type}...")
        
        full_content = title + " " + " ".join(bullets) + " " + description
        
        # Check for English contamination
        english_words = ["the", "and", "with", "for", "quality", "professional", "amazing", "perfect", "great"]
        found_english = [word for word in english_words if word.lower() in full_content.lower()]
        
        if found_english:
            glitch = f"English contamination in {test_type}: {found_english}"
            print(f"    ❌ {glitch}")
            self.glitches_found.append(glitch)
        
        # Check for proper German umlauts
        umlauts = ['ä', 'ö', 'ü', 'ß', 'Ä', 'Ö', 'Ü']
        umlaut_count = sum(full_content.count(char) for char in umlauts)
        
        if umlaut_count == 0:
            glitch = f"No German umlauts found in {test_type} - possible language generation failure"
            print(f"    ⚠️ {glitch}")
            self.glitches_found.append(glitch)
        else:
            print(f"    ✅ German umlauts found: {umlaut_count}")
        
        # Check for German-specific words
        german_words = ["der", "die", "das", "für", "mit", "und", "ist", "haben", "können", "endlich", "perfekt"]
        german_count = sum(1 for word in german_words if word in full_content.lower())
        
        if german_count < 3:
            glitch = f"Insufficient German language elements in {test_type}: only {german_count} found"
            print(f"    ⚠️ {glitch}")
            self.glitches_found.append(glitch)
        else:
            print(f"    ✅ German language elements: {german_count}")
        
        # Check A+ content language
        if aplus_content:
            aplus_text = str(aplus_content)
            aplus_english = [word for word in english_words if word.lower() in aplus_text.lower()]
            if aplus_english:
                glitch = f"English in A+ content for {test_type}: {aplus_english}"
                print(f"    ❌ {glitch}")
                self.glitches_found.append(glitch)
    
    def check_brand_tone_application(self, brand_tone, title, bullets, description):
        """Check if brand tone is properly applied in German"""
        print(f"  🎨 Checking {brand_tone} brand tone application...")
        
        # Brand tone specific word mappings for German
        tone_words = {
            "professional": ["professionell", "bewährt", "zuverlässig", "qualität", "präzision"],
            "casual": ["einfach", "super", "toll", "prima", "klasse"],
            "luxury": ["premium", "luxuriös", "elegant", "exklusiv", "raffiniert"],
            "playful": ["spaß", "cool", "clever", "kreativ", "überraschend"],
            "minimal": ["einfach", "klar", "rein", "wesentlich", "fokussiert"],
            "bold": ["kraftvoll", "stark", "intensiv", "maximal", "ultimativ"]
        }
        
        expected_words = tone_words.get(brand_tone, [])
        full_content = (title + " " + " ".join(bullets) + " " + description).lower()
        
        found_words = [word for word in expected_words if word in full_content]
        
        if len(found_words) < 2:
            glitch = f"Brand tone {brand_tone} not properly applied in German - only {len(found_words)} relevant words found"
            print(f"    ❌ {glitch}")
            self.glitches_found.append(glitch)
        else:
            print(f"    ✅ Brand tone words found: {found_words}")
    
    def check_occasion_application(self, occasion, title, bullets, description):
        """Check if occasion is properly applied in German"""
        print(f"  🎁 Checking {occasion} occasion application...")
        
        # Occasion specific word mappings for German
        occasion_words = {
            "Christmas": ["weihnachten", "geschenk", "festlich", "winter", "dezember"],
            "Valentine's Day": ["valentinstag", "liebe", "romantisch", "partner", "februar"],
            "Mother's Day": ["muttertag", "mama", "mutter", "mai", "geschenk"],
            "Father's Day": ["vatertag", "papa", "vater", "juni", "geschenk"],
            "Easter": ["ostern", "frühling", "april", "fest", "geschenk"],
            "Birthday": ["geburtstag", "feier", "geschenk", "jubiläum", "fest"],
            "Wedding": ["hochzeit", "paar", "ehe", "geschenk", "elegant"],
            "Anniversary": ["jahrestag", "jubiläum", "paar", "erinnerung", "geschenk"]
        }
        
        expected_words = occasion_words.get(occasion, [])
        full_content = (title + " " + " ".join(bullets) + " " + description).lower()
        
        found_words = [word for word in expected_words if word in full_content]
        
        if len(found_words) < 1:
            glitch = f"Occasion {occasion} not properly applied in German - no relevant words found"
            print(f"    ❌ {glitch}")
            self.glitches_found.append(glitch)
        else:
            print(f"    ✅ Occasion words found: {found_words}")
    
    def check_aplus_structure(self, test_name, aplus_content, test_type):
        """Check A+ content structure for Germany vs other markets"""
        print(f"  🖼️ Checking A+ content structure for {test_name}...")
        
        if not aplus_content:
            glitch = f"No A+ content generated for {test_name}"
            print(f"    ❌ {glitch}")
            self.glitches_found.append(glitch)
            return
        
        # Expected A+ sections
        expected_sections = ["section1_hero", "section2_features", "section3_trust", "section4_faqs"]
        missing_sections = [section for section in expected_sections if section not in aplus_content]
        
        if missing_sections:
            glitch = f"Missing A+ sections in {test_name}: {missing_sections}"
            print(f"    ❌ {glitch}")
            self.glitches_found.append(glitch)
        else:
            print(f"    ✅ All expected A+ sections present")
        
        # Check each section structure
        for section_key, section_data in aplus_content.items():
            if isinstance(section_data, dict):
                # Check for required fields
                if 'title' not in section_data:
                    glitch = f"Missing title in {section_key} for {test_name}"
                    print(f"    ❌ {glitch}")
                    self.glitches_found.append(glitch)
                
                if 'content' not in section_data:
                    glitch = f"Missing content in {section_key} for {test_name}"
                    print(f"    ❌ {glitch}")
                    self.glitches_found.append(glitch)
                
                # Check German language in A+ content
                if 'title' in section_data and section_data['title']:
                    title_text = str(section_data['title']).lower()
                    english_in_title = any(word in title_text for word in ["the", "and", "with", "for"])
                    if english_in_title:
                        glitch = f"English words in A+ {section_key} title for {test_name}"
                        print(f"    ❌ {glitch}")
                        self.glitches_found.append(glitch)
    
    def count_umlauts(self, text):
        """Count German umlauts in text"""
        umlauts = ['ä', 'ö', 'ü', 'ß', 'Ä', 'Ö', 'Ü']
        return sum(text.count(char) for char in umlauts)
    
    def count_brand_tone_words(self, brand_tone, text):
        """Count brand tone specific words"""
        tone_words = {
            "professional": ["professionell", "bewährt", "zuverlässig", "qualität"],
            "casual": ["einfach", "super", "toll", "prima"],
            "luxury": ["premium", "luxuriös", "elegant", "exklusiv"],
            "playful": ["spaß", "cool", "clever", "kreativ"],
            "minimal": ["einfach", "klar", "rein", "wesentlich"],
            "bold": ["kraftvoll", "stark", "intensiv", "maximal"]
        }
        
        words = tone_words.get(brand_tone, [])
        return sum(1 for word in words if word in text.lower())
    
    def count_occasion_references(self, occasion, text):
        """Count occasion references"""
        occasion_words = {
            "Christmas": ["weihnachten", "geschenk", "festlich"],
            "Valentine's Day": ["valentinstag", "liebe", "romantisch"],
            "Mother's Day": ["muttertag", "mama", "mutter"],
            "Father's Day": ["vatertag", "papa", "vater"],
            "Easter": ["ostern", "frühling"],
            "Birthday": ["geburtstag", "feier"],
            "Wedding": ["hochzeit", "paar", "ehe"],
            "Anniversary": ["jahrestag", "jubiläum", "paar"]
        }
        
        words = occasion_words.get(occasion, [])
        return sum(1 for word in words if word in text.lower())
    
    def compare_with_other_markets(self, product_id):
        """Compare German results with US and French markets"""
        print(f"\n🌍 Comparing German market with other markets...")
        
        markets_to_compare = [
            {"marketplace": "com", "language": "en", "name": "US"},
            {"marketplace": "fr", "language": "fr", "name": "France"},
            {"marketplace": "it", "language": "it", "name": "Italy"}
        ]
        
        comparison_results = {}
        
        for market in markets_to_compare:
            print(f"  Testing {market['name']} market...")
            
            listing_data = {
                "product": product_id,
                "marketplace": market["marketplace"],
                "marketplace_language": market["language"],
                "brand_tone": "professional",
                "platform": "amazon"
            }
            
            try:
                response = requests.post(f"{self.base_url}/api/listings/generate/", json=listing_data)
                
                if response.status_code == 200:
                    result = response.json()
                    aplus = result.get('aplus_content_plan', {})
                    
                    comparison_results[market['name']] = {
                        "aplus_sections": list(aplus.keys()) if aplus else [],
                        "section_count": len(aplus) if aplus else 0,
                        "has_hero": "section1_hero" in aplus if aplus else False,
                        "has_features": "section2_features" in aplus if aplus else False,
                        "has_trust": "section3_trust" in aplus if aplus else False,
                        "has_faqs": "section4_faqs" in aplus if aplus else False
                    }
                    print(f"    ✅ {market['name']}: {len(aplus) if aplus else 0} A+ sections")
                else:
                    print(f"    ❌ {market['name']} failed: {response.status_code}")
            except Exception as e:
                print(f"    ❌ {market['name']} error: {e}")
        
        # Compare structures
        german_aplus = self.test_results.get("brand_tone_professional", {}).get("aplus_sections", [])
        
        for market_name, market_data in comparison_results.items():
            market_sections = market_data["aplus_sections"]
            
            if set(german_aplus) != set(market_sections):
                glitch = f"A+ structure difference: Germany has {german_aplus}, {market_name} has {market_sections}"
                print(f"  ⚠️ {glitch}")
                self.glitches_found.append(glitch)
            else:
                print(f"  ✅ A+ structure matches between Germany and {market_name}")
        
        return comparison_results
    
    def generate_report(self, comparison_data=None):
        """Generate comprehensive test report"""
        print(f"\n📋 COMPREHENSIVE GERMAN MARKET TEST REPORT")
        print(f"=" * 60)
        print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total Tests Run: {len(self.test_results)}")
        print(f"Glitches Found: {len(self.glitches_found)}")
        
        # Brand tone results
        print(f"\n🎨 BRAND TONE RESULTS:")
        print(f"-" * 30)
        for brand_tone in self.brand_tones:
            key = f"brand_tone_{brand_tone}"
            if key in self.test_results:
                result = self.test_results[key]
                print(f"{brand_tone.upper()}:")
                print(f"  Title: {result['title'][:60]}...")
                print(f"  German umlauts: {result['german_umlauts_found']}")
                print(f"  Brand tone words: {result['brand_tone_words_found']}")
                print(f"  A+ sections: {len(result['aplus_sections'])}")
                print()
        
        # Occasion results  
        print(f"\n🎁 OCCASION RESULTS:")
        print(f"-" * 30)
        for occasion in self.occasions:
            key = f"occasion_{occasion}"
            if key in self.test_results:
                result = self.test_results[key]
                print(f"{occasion.upper()}:")
                print(f"  Title: {result['title'][:60]}...")
                print(f"  German umlauts: {result['german_umlauts_found']}")
                print(f"  Occasion references: {result['occasion_references']}")
                print(f"  A+ sections: {len(result['aplus_sections'])}")
                print()
        
        # Market comparison
        if comparison_data:
            print(f"\n🌍 MARKET COMPARISON:")
            print(f"-" * 30)
            for market, data in comparison_data.items():
                print(f"{market}: {data['section_count']} A+ sections")
                print(f"  Sections: {data['aplus_sections']}")
                print()
        
        # Critical glitches
        print(f"\n❌ CRITICAL GLITCHES FOUND:")
        print(f"-" * 30)
        if not self.glitches_found:
            print("✅ No critical glitches detected!")
        else:
            for i, glitch in enumerate(self.glitches_found, 1):
                print(f"{i}. {glitch}")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        print(f"-" * 30)
        
        language_glitches = [g for g in self.glitches_found if "English" in g or "umlaut" in g]
        if language_glitches:
            print("🔧 Fix German language generation:")
            for glitch in language_glitches:
                print(f"  - {glitch}")
        
        structure_glitches = [g for g in self.glitches_found if "A+" in g or "section" in g]
        if structure_glitches:
            print("🔧 Fix A+ content structure:")
            for glitch in structure_glitches:
                print(f"  - {glitch}")
        
        tone_glitches = [g for g in self.glitches_found if "Brand tone" in g or "Occasion" in g]
        if tone_glitches:
            print("🔧 Fix brand tone/occasion application:")
            for glitch in tone_glitches:
                print(f"  - {glitch}")
        
        # Save report to file
        report_file = f"german_market_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report_data = {
            "test_date": datetime.now().isoformat(),
            "total_tests": len(self.test_results),
            "glitches_count": len(self.glitches_found),
            "test_results": self.test_results,
            "glitches_found": self.glitches_found,
            "market_comparison": comparison_data
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Report saved to: {report_file}")
    
    def run_comprehensive_test(self):
        """Run all tests for German marketplace"""
        print("🚀 Starting Comprehensive German Market Testing...")
        print("=" * 60)
        
        # Setup test product
        product_id = self.setup_test_product()
        if not product_id:
            print("❌ Cannot proceed without test product")
            return
        
        # Test all brand tones
        print(f"\n📍 Phase 1: Testing Brand Tones for Germany")
        for brand_tone in self.brand_tones:
            try:
                self.test_brand_tone(product_id, brand_tone)
                time.sleep(2)  # Rate limiting
            except Exception as e:
                print(f"❌ Brand tone {brand_tone} failed: {e}")
        
        # Test all occasions  
        print(f"\n📍 Phase 2: Testing Occasions for Germany")
        for occasion in self.occasions:
            try:
                self.test_occasion(product_id, occasion)
                time.sleep(2)  # Rate limiting
            except Exception as e:
                print(f"❌ Occasion {occasion} failed: {e}")
        
        # Compare with other markets
        print(f"\n📍 Phase 3: Cross-Market Comparison")
        comparison_data = self.compare_with_other_markets(product_id)
        
        # Generate report
        print(f"\n📍 Phase 4: Generating Report")
        self.generate_report(comparison_data)
        
        print(f"\n🎉 Comprehensive German Market Testing Complete!")
        print(f"📊 Summary: {len(self.test_results)} tests completed, {len(self.glitches_found)} glitches found")


if __name__ == "__main__":
    tester = GermanMarketTester()
    tester.run_comprehensive_test()