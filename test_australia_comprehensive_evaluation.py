#!/usr/bin/env python3
"""
🇦🇺 AUSTRALIA MARKETPLACE COMPREHENSIVE EVALUATION
Testing Australia marketplace implementation with Premium Wireless Gaming Headset Pro
"""

import requests
import json
import time
from datetime import datetime
import os

# Test Configuration
BASE_URL = "http://127.0.0.1:8000"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

class AustraliaMarketplaceEvaluator:
    def __init__(self):
        self.session = requests.Session()
        self.results = {}
        
    def create_test_product(self):
        """Create test product for Australia marketplace"""
        print("Creating Australia test product...")
        
        product_data = {
            "name": "Premium Wireless Gaming Headset Pro",
            "brand_name": "AudioElite",
            "brand_tone": "luxury",
            "target_platform": "amazon",
            "marketplace": "au",
            "marketplace_language": "en-au",
            "price": 299.99,
            "categories": "Electronics, Gaming, Audio",
            "target_keywords": "wireless gaming headset, premium gaming audio, noise cancelling headset, RGB gaming headset, professional gaming gear",
            "description": "Professional-grade wireless gaming headset with advanced noise cancellation, premium audio drivers, RGB lighting, and extended battery life designed for serious gamers.",
            "occasion": "australia_day",
            "target_audience": "Serious gamers and audio enthusiasts who demand premium quality and performance",
            "features": "Wireless connectivity, Active noise cancellation, RGB lighting, 30+ hour battery, Premium audio drivers, Comfortable design"
        }
        
        try:
            response = self.session.post(f"{BASE_URL}/api/core/products/", json=product_data)
            if response.status_code == 201:
                product = response.json()
                print(f"SUCCESS: Product created successfully: ID {product['id']}")
                return product
            else:
                print(f"ERROR: Failed to create product: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except Exception as e:
            print(f"ERROR: Error creating product: {str(e)}")
            return None
    
    def generate_australia_listing(self, product_id):
        """Generate Australia marketplace listing"""
        print("Generating Australia marketplace listing...")
        
        listing_data = {
            "marketplace": "au",  # Australia
            "language": "en-au",  # Australian English
            "occasion": "australia_day",  # Australia Day occasion
            "brand_tone": "luxury",  # Luxury brand tone
            "target_audience": "gaming_enthusiasts"
        }
        
        try:
            response = self.session.post(f"{BASE_URL}/api/listings/generate-clean/{product_id}/amazon/", json=listing_data)
            if response.status_code in [200, 201]:
                result = response.json()
                print("SUCCESS: Australia listing generated successfully!")
                # If we have a listing ID, we need to fetch the actual listing data
                if 'id' in result:
                    listing_id = result['id']
                    # Fetch the actual listing data
                    listing_response = self.session.get(f"{BASE_URL}/api/listings/generated/{listing_id}/")
                    if listing_response.status_code == 200:
                        return listing_response.json()
                return result
            else:
                print(f"ERROR: Failed to generate listing: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except Exception as e:
            print(f"ERROR: Error generating listing: {str(e)}")
            return None
    
    def analyze_australia_quality(self, listing_data):
        """Comprehensive quality analysis for Australia listing"""
        print("Analyzing Australia listing quality...")
        
        analysis = {
            "timestamp": TIMESTAMP,
            "marketplace": "Australia (amazon.com.au)",
            "language": "English (en-au)",
            "occasion": "Australia Day",
            "brand_tone": "Luxury",
            "cultural_analysis": {},
            "localization_analysis": {},
            "aplus_content_analysis": {},
            "competitive_analysis": {},
            "quality_scores": {},
            "overall_assessment": {}
        }
        
        # Cultural Elements Analysis
        analysis["cultural_analysis"] = self.analyze_australian_cultural_elements(listing_data)
        
        # Localization Analysis
        analysis["localization_analysis"] = self.analyze_australian_localization(listing_data)
        
        # A+ Content Analysis
        analysis["aplus_content_analysis"] = self.analyze_aplus_content(listing_data)
        
        # Competitive Analysis
        analysis["competitive_analysis"] = self.perform_competitive_analysis(listing_data)
        
        # Quality Scoring
        analysis["quality_scores"] = self.calculate_quality_scores(listing_data, analysis)
        
        # Overall Assessment
        analysis["overall_assessment"] = self.generate_overall_assessment(analysis)
        
        return analysis
    
    def analyze_australian_cultural_elements(self, listing_data):
        """Analyze Australian cultural elements integration"""
        cultural_elements = {
            "australia_day_references": 0,
            "aussie_slang_usage": 0,
            "mateship_references": 0,
            "fair_dinkum_usage": 0,
            "bbq_culture_references": 0,
            "outback_references": 0,
            "iconic_landmarks": 0,
            "australian_lifestyle": 0
        }
        
        # Get all text content
        all_text = ""
        if 'productTitle' in listing_data:
            all_text += listing_data['productTitle'] + " "
        if 'productDescription' in listing_data:
            all_text += listing_data['productDescription'] + " "
        if 'bulletPoints' in listing_data:
            all_text += " ".join(listing_data['bulletPoints']) + " "
        if 'aPlusContentPlan' in listing_data:
            all_text += str(listing_data['aPlusContentPlan']) + " "
        
        all_text = all_text.lower()
        
        # Check for Australian cultural elements
        if 'australia day' in all_text:
            cultural_elements["australia_day_references"] += all_text.count('australia day')
        if any(word in all_text for word in ['aussie', 'oz', 'straya']):
            cultural_elements["aussie_slang_usage"] += 1
        if 'mateship' in all_text or 'mate' in all_text:
            cultural_elements["mateship_references"] += 1
        if 'fair dinkum' in all_text:
            cultural_elements["fair_dinkum_usage"] += all_text.count('fair dinkum')
        if any(word in all_text for word in ['bbq', 'barbecue', 'barbie']):
            cultural_elements["bbq_culture_references"] += 1
        if 'outback' in all_text:
            cultural_elements["outback_references"] += all_text.count('outback')
        if any(landmark in all_text for landmark in ['sydney harbour', 'opera house', 'uluru', 'great barrier reef', 'bondi']):
            cultural_elements["iconic_landmarks"] += 1
        if any(word in all_text for word in ['extreme climate', 'outdoor lifestyle', 'coastal living']):
            cultural_elements["australian_lifestyle"] += 1
        
        # Calculate cultural integration score
        total_elements = sum(cultural_elements.values())
        cultural_score = min(10, total_elements * 1.5)  # Cap at 10
        
        return {
            "elements_found": cultural_elements,
            "total_cultural_elements": total_elements,
            "cultural_integration_score": round(cultural_score, 1),
            "assessment": "Excellent" if cultural_score >= 8 else "Good" if cultural_score >= 6 else "Fair" if cultural_score >= 4 else "Poor"
        }
    
    def analyze_australian_localization(self, listing_data):
        """Analyze Australian English localization quality"""
        localization_aspects = {
            "currency_format": False,
            "australian_spelling": 0,
            "local_standards": 0,
            "measurement_units": 0,
            "pricing_context": False,
            "shipping_references": 0
        }
        
        all_text = ""
        if 'productTitle' in listing_data:
            all_text += listing_data['productTitle'] + " "
        if 'productDescription' in listing_data:
            all_text += listing_data['productDescription'] + " "
        if 'bulletPoints' in listing_data:
            all_text += " ".join(listing_data['bulletPoints']) + " "
        
        # Check for AUD currency
        if 'aud' in all_text.lower() or '$' in all_text:
            localization_aspects["currency_format"] = True
        
        # Check Australian spelling (colour vs color, etc.)
        australian_words = ['colour', 'flavour', 'honour', 'centre', 'theatre', 'realise', 'organise']
        for word in australian_words:
            if word in all_text.lower():
                localization_aspects["australian_spelling"] += 1
        
        # Check for local standards (ACMA, Australian standards)
        if any(standard in all_text.lower() for standard in ['acma', 'australian standard', 'aus standard']):
            localization_aspects["local_standards"] += 1
        
        # Check for metric measurements
        if any(unit in all_text.lower() for unit in ['cm', 'mm', 'kg', 'g', 'ml', 'l']):
            localization_aspects["measurement_units"] += 1
        
        # Check for Australian pricing context
        if 'aud' in all_text.lower():
            localization_aspects["pricing_context"] = True
        
        # Check for shipping references
        if any(term in all_text.lower() for term in ['australia wide', 'aussie shipping', 'local delivery']):
            localization_aspects["shipping_references"] += 1
        
        # Calculate localization score
        score_factors = [
            localization_aspects["currency_format"] * 2,
            min(3, localization_aspects["australian_spelling"]),
            localization_aspects["local_standards"] * 2,
            min(2, localization_aspects["measurement_units"]),
            localization_aspects["pricing_context"] * 1,
            min(2, localization_aspects["shipping_references"])
        ]
        
        localization_score = sum(score_factors)
        max_score = 12
        normalized_score = (localization_score / max_score) * 10
        
        return {
            "aspects_analyzed": localization_aspects,
            "localization_score": round(normalized_score, 1),
            "assessment": "Excellent" if normalized_score >= 8 else "Good" if normalized_score >= 6 else "Fair" if normalized_score >= 4 else "Poor"
        }
    
    def analyze_aplus_content(self, listing_data):
        """Analyze A+ content quality and structure"""
        aplus_analysis = {
            "sections_count": 0,
            "has_hero_section": False,
            "has_features_section": False,
            "has_comparison_section": False,
            "has_lifestyle_section": False,
            "has_trust_section": False,
            "has_specifications_section": False,
            "has_faq_section": False,
            "has_guarantee_section": False,
            "english_image_descriptions": 0,
            "australian_context_images": 0
        }
        
        if 'aPlusContentPlan' in listing_data:
            aplus_content = str(listing_data['aPlusContentPlan']).lower()
            
            # Count sections
            sections = ['hero', 'features', 'comparison', 'lifestyle', 'trust', 'specifications', 'faq', 'guarantee']
            for section in sections:
                if section in aplus_content:
                    aplus_analysis[f"has_{section}_section"] = True
                    aplus_analysis["sections_count"] += 1
            
            # Check for ENGLISH image descriptions
            if 'english:' in aplus_content:
                aplus_analysis["english_image_descriptions"] = aplus_content.count('english:')
            
            # Check for Australian context in images
            australian_contexts = ['australian', 'aussie', 'sydney', 'melbourne', 'queensland', 'bondi', 'outback']
            for context in australian_contexts:
                if context in aplus_content:
                    aplus_analysis["australian_context_images"] += 1
        
        # Calculate A+ content score
        section_score = min(8, aplus_analysis["sections_count"]) * 1.25  # 8 sections max, 10 points
        english_desc_score = min(8, aplus_analysis["english_image_descriptions"]) * 0.5  # 4 points max
        australian_context_score = min(8, aplus_analysis["australian_context_images"]) * 0.5  # 4 points max
        
        total_score = section_score + english_desc_score + australian_context_score
        
        return {
            "analysis_details": aplus_analysis,
            "sections_found": aplus_analysis["sections_count"],
            "english_descriptions": aplus_analysis["english_image_descriptions"],
            "australian_context": aplus_analysis["australian_context_images"],
            "aplus_score": round(total_score, 1),
            "assessment": "Excellent" if total_score >= 8 else "Good" if total_score >= 6 else "Fair" if total_score >= 4 else "Poor"
        }
    
    def perform_competitive_analysis(self, listing_data):
        """Compare against Helium 10, Jasper AI, and Copy Monkey standards"""
        competitive_metrics = {
            "title_optimization": 0,
            "keyword_density": 0,
            "bullet_point_quality": 0,
            "description_engagement": 0,
            "emotional_triggers": 0,
            "conversion_elements": 0,
            "brand_positioning": 0,
            "market_differentiation": 0
        }
        
        # Analyze title (max 200 chars, keyword-rich)
        if 'productTitle' in listing_data:
            title = listing_data['productTitle']
            title_score = 0
            if len(title) <= 200:
                title_score += 2
            if len(title) >= 100:
                title_score += 2
            # Check for key gaming terms
            gaming_terms = ['gaming', 'wireless', 'premium', 'pro', 'audio', 'headset']
            title_score += sum(1 for term in gaming_terms if term.lower() in title.lower())
            competitive_metrics["title_optimization"] = min(10, title_score)
        
        # Analyze keyword density
        if 'seoKeywords' in listing_data:
            keywords = listing_data['seoKeywords']
            if isinstance(keywords, list):
                keyword_count = len(keywords)
            else:
                keyword_count = len(str(keywords).split(','))
            competitive_metrics["keyword_density"] = min(10, keyword_count * 0.5)
        
        # Analyze bullet points
        if 'bulletPoints' in listing_data:
            bullets = listing_data['bulletPoints']
            bullet_score = 0
            if isinstance(bullets, list):
                bullet_score += min(5, len(bullets))  # 5 bullets ideal
                for bullet in bullets:
                    if len(bullet) > 100:  # Substantial content
                        bullet_score += 1
            competitive_metrics["bullet_point_quality"] = min(10, bullet_score)
        
        # Analyze description engagement
        if 'productDescription' in listing_data:
            description = listing_data['productDescription']
            desc_score = 0
            if len(description) > 1000:
                desc_score += 3
            if len(description) > 1500:
                desc_score += 2
            # Check for engaging words
            engaging_words = ['discover', 'experience', 'premium', 'professional', 'advanced', 'innovative']
            desc_score += sum(1 for word in engaging_words if word.lower() in description.lower())
            competitive_metrics["description_engagement"] = min(10, desc_score)
        
        # Analyze emotional triggers
        all_text = str(listing_data).lower()
        emotional_words = ['premium', 'professional', 'luxury', 'exclusive', 'superior', 'elite', 'exceptional', 'outstanding']
        emotional_score = sum(1 for word in emotional_words if word in all_text)
        competitive_metrics["emotional_triggers"] = min(10, emotional_score * 1.5)
        
        # Analyze conversion elements
        conversion_words = ['guarantee', 'warranty', 'satisfaction', 'money back', 'free shipping', 'certified']
        conversion_score = sum(1 for word in conversion_words if word in all_text)
        competitive_metrics["conversion_elements"] = min(10, conversion_score * 2)
        
        # Analyze brand positioning
        brand_words = ['audiolite', 'premium', 'professional', 'luxury', 'elite']
        brand_score = sum(1 for word in brand_words if word in all_text)
        competitive_metrics["brand_positioning"] = min(10, brand_score * 2)
        
        # Market differentiation
        diff_words = ['unique', 'exclusive', 'innovative', 'advanced', 'cutting-edge', 'revolutionary']
        diff_score = sum(1 for word in diff_words if word in all_text)
        competitive_metrics["market_differentiation"] = min(10, diff_score * 1.5)
        
        # Calculate overall competitive score
        total_competitive_score = sum(competitive_metrics.values()) / len(competitive_metrics)
        
        return {
            "individual_metrics": competitive_metrics,
            "overall_competitive_score": round(total_competitive_score, 1),
            "helium10_comparison": "Superior" if total_competitive_score >= 8 else "Competitive" if total_competitive_score >= 6 else "Needs Improvement",
            "jasper_ai_comparison": "Superior" if total_competitive_score >= 7.5 else "Competitive" if total_competitive_score >= 5.5 else "Needs Improvement",
            "copy_monkey_comparison": "Superior" if total_competitive_score >= 7 else "Competitive" if total_competitive_score >= 5 else "Needs Improvement"
        }
    
    def calculate_quality_scores(self, listing_data, analysis):
        """Calculate comprehensive quality scores"""
        scores = {
            "cultural_integration": analysis["cultural_analysis"]["cultural_integration_score"],
            "localization_quality": analysis["localization_analysis"]["localization_score"],
            "aplus_content": analysis["aplus_content_analysis"]["aplus_score"],
            "competitive_positioning": analysis["competitive_analysis"]["overall_competitive_score"]
        }
        
        # Content quality scores
        content_scores = {
            "title_quality": 0,
            "description_quality": 0,
            "bullet_quality": 0,
            "keyword_optimization": 0
        }
        
        # Title quality (length, keywords, readability)
        if 'productTitle' in listing_data:
            title = listing_data['productTitle']
            title_score = 0
            if 80 <= len(title) <= 200:
                title_score += 3
            if any(word in title.lower() for word in ['wireless', 'gaming', 'premium', 'pro']):
                title_score += 3
            if 'australia' in title.lower() or 'aussie' in title.lower():
                title_score += 2
            content_scores["title_quality"] = min(10, title_score)
        
        # Description quality
        if 'productDescription' in listing_data:
            desc = listing_data['productDescription']
            desc_score = 0
            if len(desc) > 1000:
                desc_score += 3
            if 'australia' in desc.lower():
                desc_score += 2
            if any(word in desc.lower() for word in ['premium', 'professional', 'luxury']):
                desc_score += 3
            content_scores["description_quality"] = min(10, desc_score)
        
        # Bullet quality
        if 'bulletPoints' in listing_data:
            bullets = listing_data['bulletPoints']
            bullet_score = 0
            if isinstance(bullets, list) and len(bullets) >= 5:
                bullet_score += 5
                for bullet in bullets:
                    if len(bullet) > 100:
                        bullet_score += 1
            content_scores["bullet_quality"] = min(10, bullet_score)
        
        # Keyword optimization
        if 'seoKeywords' in listing_data:
            keywords = listing_data['seoKeywords']
            keyword_score = 0
            if isinstance(keywords, list):
                keyword_score = min(10, len(keywords) * 0.5)
            else:
                keyword_score = min(10, len(str(keywords).split(',')) * 0.5)
            content_scores["keyword_optimization"] = keyword_score
        
        # Combine all scores
        all_scores = {**scores, **content_scores}
        overall_score = sum(all_scores.values()) / len(all_scores)
        
        return {
            "individual_scores": all_scores,
            "overall_quality_score": round(overall_score, 1),
            "grade": self.get_quality_grade(overall_score),
            "strengths": self.identify_strengths(all_scores),
            "areas_for_improvement": self.identify_improvements(all_scores)
        }
    
    def get_quality_grade(self, score):
        """Convert score to letter grade"""
        if score >= 9:
            return "A+"
        elif score >= 8:
            return "A"
        elif score >= 7:
            return "B+"
        elif score >= 6:
            return "B"
        elif score >= 5:
            return "C+"
        elif score >= 4:
            return "C"
        else:
            return "D"
    
    def identify_strengths(self, scores):
        """Identify top performing areas"""
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [f"{area.replace('_', ' ').title()}: {score}/10" for area, score in sorted_scores[:3]]
    
    def identify_improvements(self, scores):
        """Identify areas needing improvement"""
        sorted_scores = sorted(scores.items(), key=lambda x: x[1])
        return [f"{area.replace('_', ' ').title()}: {score}/10" for area, score in sorted_scores[:3] if score < 7]
    
    def generate_overall_assessment(self, analysis):
        """Generate comprehensive overall assessment"""
        overall_score = analysis["quality_scores"]["overall_quality_score"]
        
        assessment = {
            "overall_score": f"{overall_score}/10",
            "grade": analysis["quality_scores"]["grade"],
            "market_readiness": "Excellent" if overall_score >= 8 else "Good" if overall_score >= 6 else "Needs Improvement",
            "competitive_position": analysis["competitive_analysis"]["helium10_comparison"],
            "cultural_adaptation": analysis["cultural_analysis"]["assessment"],
            "localization_quality": analysis["localization_analysis"]["assessment"],
            "recommendation": self.get_recommendation(overall_score),
            "next_steps": self.get_next_steps(analysis)
        }
        
        return assessment
    
    def get_recommendation(self, score):
        """Get recommendation based on score"""
        if score >= 9:
            return "Outstanding! This listing exceeds industry standards and is ready for immediate deployment."
        elif score >= 8:
            return "Excellent quality! Minor optimizations could push this to 10/10 perfection."
        elif score >= 7:
            return "Good quality listing with solid foundation. Some enhancements recommended."
        elif score >= 6:
            return "Acceptable quality but needs improvement to compete effectively."
        else:
            return "Significant improvements required before market deployment."
    
    def get_next_steps(self, analysis):
        """Generate actionable next steps"""
        steps = []
        
        if analysis["quality_scores"]["individual_scores"]["cultural_integration"] < 7:
            steps.append("Enhance Australian cultural elements and local references")
        
        if analysis["quality_scores"]["individual_scores"]["localization_quality"] < 7:
            steps.append("Improve Australian English localization and local standards")
        
        if analysis["aplus_content_analysis"]["aplus_score"] < 8:
            steps.append("Expand A+ content to include all 8 recommended sections")
        
        if analysis["competitive_analysis"]["overall_competitive_score"] < 7:
            steps.append("Strengthen competitive positioning and unique value propositions")
        
        if not steps:
            steps.append("Fine-tune minor elements to achieve perfect 10/10 score")
        
        return steps
    
    def save_results(self, analysis, listing_data):
        """Save analysis results to files"""
        # Save detailed analysis
        analysis_filename = f"australia_comprehensive_analysis_{TIMESTAMP}.json"
        with open(analysis_filename, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        # Save listing HTML
        if 'aPlusContentPlan' in listing_data:
            html_content = self.generate_html_preview(listing_data, analysis)
            html_filename = f"australia_listing_preview_{TIMESTAMP}.html"
            with open(html_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
        
        print(f"SUCCESS: Results saved:")
        print(f"   - Analysis: {analysis_filename}")
        if 'aPlusContentPlan' in listing_data:
            print(f"   - HTML Preview: {html_filename}")
        
        return analysis_filename, html_filename if 'aPlusContentPlan' in listing_data else None
    
    def generate_html_preview(self, listing_data, analysis):
        """Generate HTML preview of the listing"""
        overall_score = analysis["quality_scores"]["overall_quality_score"]
        grade = analysis["quality_scores"]["grade"]
        
        html = f"""
<!DOCTYPE html>
<html lang="en-au">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🇦🇺 Australia Marketplace Listing - Premium Wireless Gaming Headset Pro</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #e6f3ff 0%, #ffffff 100%);
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .quality-badge {{
            display: inline-block;
            background: {"#00C851" if overall_score >= 8 else "#FF8800" if overall_score >= 6 else "#FF4444"};
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            font-weight: bold;
            margin-top: 10px;
        }}
        .section {{
            padding: 30px;
            border-bottom: 1px solid #eee;
        }}
        .section:last-child {{
            border-bottom: none;
        }}
        .section h2 {{
            color: #FF6B35;
            border-bottom: 2px solid #FF6B35;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .bullet-points {{
            list-style: none;
            padding: 0;
        }}
        .bullet-points li {{
            background: #f8f9fa;
            margin: 10px 0;
            padding: 15px;
            border-left: 4px solid #FF6B35;
            border-radius: 5px;
        }}
        .aplus-section {{
            background: #f8f9fa;
            margin: 20px 0;
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #FF6B35;
        }}
        .score-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .score-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .score-value {{
            font-size: 2em;
            font-weight: bold;
            color: #FF6B35;
        }}
        .australian-flag {{
            font-size: 2em;
            margin-right: 10px;
        }}
        .competitive-comparison {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin: 20px 0;
        }}
        .competitor-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #ddd;
            text-align: center;
        }}
        .superior {{ border-color: #00C851; background: #f8fff8; }}
        .competitive {{ border-color: #FF8800; background: #fff8f0; }}
        .needs-improvement {{ border-color: #FF4444; background: #fff8f8; }}
        .cultural-elements {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 20px 0;
        }}
        .cultural-tag {{
            background: #FF6B35;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><span class="australian-flag">🇦🇺</span>Australia Marketplace Evaluation</h1>
            <h2>Premium Wireless Gaming Headset Pro by AudioElite</h2>
            <div class="quality-badge">Overall Quality Score: {overall_score}/10 ({grade})</div>
        </div>
        
        <div class="section">
            <h2>📋 Product Title</h2>
            <p style="font-size: 1.2em; font-weight: bold; color: #333;">
                {listing_data.get('productTitle', 'N/A')}
            </p>
        </div>
        
        <div class="section">
            <h2>📝 Product Description</h2>
            <p>{listing_data.get('productDescription', 'N/A')}</p>
        </div>
        
        <div class="section">
            <h2>🎯 Key Features</h2>
            <ul class="bullet-points">
        """
        
        if 'bulletPoints' in listing_data:
            for bullet in listing_data['bulletPoints']:
                html += f"<li>{bullet}</li>"
        
        html += f"""
            </ul>
        </div>
        
        <div class="section">
            <h2>📊 Quality Analysis Dashboard</h2>
            <div class="score-grid">
                <div class="score-card">
                    <div class="score-value">{analysis['cultural_analysis']['cultural_integration_score']}/10</div>
                    <h4>Cultural Integration</h4>
                    <p>{analysis['cultural_analysis']['assessment']}</p>
                </div>
                <div class="score-card">
                    <div class="score-value">{analysis['localization_analysis']['localization_score']}/10</div>
                    <h4>Australian Localization</h4>
                    <p>{analysis['localization_analysis']['assessment']}</p>
                </div>
                <div class="score-card">
                    <div class="score-value">{analysis['aplus_content_analysis']['aplus_score']}/10</div>
                    <h4>A+ Content Quality</h4>
                    <p>{analysis['aplus_content_analysis']['assessment']}</p>
                </div>
                <div class="score-card">
                    <div class="score-value">{analysis['competitive_analysis']['overall_competitive_score']}/10</div>
                    <h4>Competitive Position</h4>
                    <p>{analysis['competitive_analysis']['helium10_comparison']}</p>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>🇦🇺 Australian Cultural Elements</h2>
            <div class="cultural-elements">
        """
        
        cultural_elements = analysis['cultural_analysis']['elements_found']
        for element, count in cultural_elements.items():
            if count > 0:
                html += f'<span class="cultural-tag">{element.replace("_", " ").title()}: {count}</span>'
        
        html += f"""
            </div>
            <p><strong>Total Cultural Elements Found:</strong> {analysis['cultural_analysis']['total_cultural_elements']}</p>
        </div>
        
        <div class="section">
            <h2>🥊 Competitive Analysis</h2>
            <div class="competitive-comparison">
                <div class="competitor-card {analysis['competitive_analysis']['helium10_comparison'].lower().replace(' ', '-')}">
                    <h4>vs Helium 10</h4>
                    <p><strong>{analysis['competitive_analysis']['helium10_comparison']}</strong></p>
                </div>
                <div class="competitor-card {analysis['competitive_analysis']['jasper_ai_comparison'].lower().replace(' ', '-')}">
                    <h4>vs Jasper AI</h4>
                    <p><strong>{analysis['competitive_analysis']['jasper_ai_comparison']}</strong></p>
                </div>
                <div class="competitor-card {analysis['competitive_analysis']['copy_monkey_comparison'].lower().replace(' ', '-')}">
                    <h4>vs Copy Monkey</h4>
                    <p><strong>{analysis['competitive_analysis']['copy_monkey_comparison']}</strong></p>
                </div>
            </div>
        </div>
        """
        
        if 'aPlusContentPlan' in listing_data:
            html += f"""
        <div class="section">
            <h2>🎨 A+ Content Preview</h2>
            <div class="aplus-section">
                <h3>A+ Content Plan</h3>
                <pre style="white-space: pre-wrap; background: #f8f9fa; padding: 15px; border-radius: 5px;">
{listing_data['aPlusContentPlan']}
                </pre>
            </div>
            <p><strong>Sections Found:</strong> {analysis['aplus_content_analysis']['sections_found']}/8</p>
            <p><strong>ENGLISH Image Descriptions:</strong> {analysis['aplus_content_analysis']['english_descriptions']}</p>
            <p><strong>Australian Context Images:</strong> {analysis['aplus_content_analysis']['australian_context']}</p>
        </div>
            """
        
        html += f"""
        <div class="section">
            <h2>💪 Strengths & Improvements</h2>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px;">
                <div>
                    <h4 style="color: #00C851;">🌟 Top Strengths</h4>
                    <ul>
        """
        
        for strength in analysis['quality_scores']['strengths']:
            html += f"<li>{strength}</li>"
        
        html += """
                    </ul>
                </div>
                <div>
                    <h4 style="color: #FF4444;">🔧 Areas for Improvement</h4>
                    <ul>
        """
        
        if analysis['quality_scores']['areas_for_improvement']:
            for improvement in analysis['quality_scores']['areas_for_improvement']:
                html += f"<li>{improvement}</li>"
        else:
            html += "<li>No significant improvements needed!</li>"
        
        html += f"""
                    </ul>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>🎯 Recommendations</h2>
            <p><strong>Assessment:</strong> {analysis['overall_assessment']['recommendation']}</p>
            <h4>Next Steps:</h4>
            <ul>
        """
        
        for step in analysis['overall_assessment']['next_steps']:
            html += f"<li>{step}</li>"
        
        html += f"""
            </ul>
        </div>
        
        <div class="section">
            <h2>📈 Final Assessment</h2>
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #FF6B35;">
                <p><strong>Overall Score:</strong> {analysis['overall_assessment']['overall_score']}</p>
                <p><strong>Grade:</strong> {analysis['overall_assessment']['grade']}</p>
                <p><strong>Market Readiness:</strong> {analysis['overall_assessment']['market_readiness']}</p>
                <p><strong>Competitive Position:</strong> {analysis['overall_assessment']['competitive_position']}</p>
                <p><strong>Cultural Adaptation:</strong> {analysis['overall_assessment']['cultural_adaptation']}</p>
                <p><strong>Localization Quality:</strong> {analysis['overall_assessment']['localization_quality']}</p>
            </div>
        </div>
        
        <div class="header" style="background: linear-gradient(135deg, #00C851 0%, #00A652 100%);">
            <h3>🇦🇺 Australia Marketplace Implementation Complete</h3>
            <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>
    </div>
</body>
</html>
        """
        
        return html
    
    def run_comprehensive_evaluation(self):
        """Run complete Australia marketplace evaluation"""
        print("AUSTRALIA MARKETPLACE COMPREHENSIVE EVALUATION")
        print("=" * 70)
        
        # Step 1: Create test product
        product = self.create_test_product()
        if not product:
            print("ERROR: Failed to create test product. Exiting.")
            return None
        
        # Step 2: Generate Australia listing
        listing_data = self.generate_australia_listing(product['id'])
        if not listing_data:
            print("ERROR: Failed to generate Australia listing. Exiting.")
            return None
        
        # Step 3: Comprehensive quality analysis
        analysis = self.analyze_australia_quality(listing_data)
        
        # Step 4: Save results
        analysis_file, html_file = self.save_results(analysis, listing_data)
        
        # Step 5: Print summary
        self.print_summary(analysis, analysis_file, html_file)
        
        return analysis
    
    def print_summary(self, analysis, analysis_file, html_file):
        """Print comprehensive summary"""
        print("\n" + "=" * 70)
        print("AUSTRALIA MARKETPLACE EVALUATION COMPLETE")
        print("=" * 70)
        
        overall_score = analysis['quality_scores']['overall_quality_score']
        grade = analysis['quality_scores']['grade']
        
        print(f"OVERALL RESULTS:")
        print(f"   Score: {overall_score}/10")
        print(f"   Grade: {grade}")
        print(f"   Assessment: {analysis['overall_assessment']['market_readiness']}")
        
        print(f"\nDETAILED SCORES:")
        for metric, score in analysis['quality_scores']['individual_scores'].items():
            print(f"   {metric.replace('_', ' ').title()}: {score}/10")
        
        print(f"\nCULTURAL INTEGRATION:")
        print(f"   Score: {analysis['cultural_analysis']['cultural_integration_score']}/10")
        print(f"   Elements Found: {analysis['cultural_analysis']['total_cultural_elements']}")
        print(f"   Assessment: {analysis['cultural_analysis']['assessment']}")
        
        print(f"\nLOCALIZATION QUALITY:")
        print(f"   Score: {analysis['localization_analysis']['localization_score']}/10")
        print(f"   Assessment: {analysis['localization_analysis']['assessment']}")
        
        print(f"\nA+ CONTENT ANALYSIS:")
        print(f"   Score: {analysis['aplus_content_analysis']['aplus_score']}/10")
        print(f"   Sections: {analysis['aplus_content_analysis']['sections_found']}/8")
        print(f"   ENGLISH Descriptions: {analysis['aplus_content_analysis']['english_descriptions']}")
        print(f"   Australian Context: {analysis['aplus_content_analysis']['australian_context']}")
        
        print(f"\nCOMPETITIVE COMPARISON:")
        print(f"   vs Helium 10: {analysis['competitive_analysis']['helium10_comparison']}")
        print(f"   vs Jasper AI: {analysis['competitive_analysis']['jasper_ai_comparison']}")
        print(f"   vs Copy Monkey: {analysis['competitive_analysis']['copy_monkey_comparison']}")
        
        print(f"\nTOP STRENGTHS:")
        for strength in analysis['quality_scores']['strengths']:
            print(f"   SUCCESS: {strength}")
        
        if analysis['quality_scores']['areas_for_improvement']:
            print(f"\nIMPROVEMENTS NEEDED:")
            for improvement in analysis['quality_scores']['areas_for_improvement']:
                print(f"   WARNING: {improvement}")
        else:
            print(f"\nNO SIGNIFICANT IMPROVEMENTS NEEDED!")
        
        print(f"\nFILES GENERATED:")
        print(f"   Analysis: {analysis_file}")
        if html_file:
            print(f"   HTML Preview: {html_file}")
        
        print(f"\nRECOMMENDATION:")
        print(f"   {analysis['overall_assessment']['recommendation']}")
        
        print("\n" + "=" * 70)
        print("AUSTRALIA MARKETPLACE READY FOR PRIME TIME!")
        print("=" * 70)

if __name__ == "__main__":
    evaluator = AustraliaMarketplaceEvaluator()
    evaluator.run_comprehensive_evaluation()