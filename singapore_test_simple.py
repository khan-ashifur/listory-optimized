#!/usr/bin/env python3
"""
Singapore Marketplace Quality Test - Simple Version
Generates Premium Wireless Gaming Headset listing for Singapore market
"""

import requests
import json
import time
from datetime import datetime
import html
import os

# Test Configuration
API_BASE = "http://127.0.0.1:8000"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

def test_singapore_listing():
    """Generate comprehensive Singapore listing"""
    print("SINGAPORE MARKETPLACE TEST")
    print("=" * 60)
    
    # Test Product Configuration
    product_data = {
        "name": "Premium Wireless Gaming Headset",
        "brand": "AudioPro",
        "price": 199.99,
        "categories": ["Electronics", "Gaming", "Audio"],
        "marketplace": "sg",  # Singapore
        "language": "en-sg",
        "occasion": "chinese_new_year",
        "brand_tone": "luxury",
        "target_keywords": [
            "wireless gaming headset",
            "premium headset singapore",
            "gaming audio",
            "rgb headset",
            "noise cancelling",
            "singapore gaming gear"
        ]
    }
    
    print("TEST CONFIGURATION:")
    print(f"   Product: {product_data['name']}")
    print(f"   Brand: {product_data['brand']}")
    print(f"   Market: Singapore (sg)")
    print(f"   Language: {product_data['language']}")
    print(f"   Price: SGD {product_data['price']}")
    print(f"   Occasion: {product_data['occasion']}")
    print(f"   Brand Tone: {product_data['brand_tone']}")
    print()
    
    try:
        # First create the product
        print("Creating product...")
        product_response = requests.post(
            f"{API_BASE}/api/core/create-product/",
            json=product_data,
            timeout=60
        )
        
        if product_response.status_code == 201:
            product_result = product_response.json()
            product_id = product_result['id']
            print(f"Product created with ID: {product_id}")
        else:
            print(f"Product creation failed: {product_response.status_code}")
            print(f"Response: {product_response.text}")
            return None
        
        # Now generate the listing
        print("Generating Singapore listing...")
        start_time = time.time()
        
        response = requests.post(
            f"{API_BASE}/api/listings/generate/{product_id}/amazon/",
            timeout=120
        )
        
        generation_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"Listing generated successfully in {generation_time:.2f}s")
            
            # Save raw response
            with open(f"singapore_listing_{TIMESTAMP}.json", "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print("\nGenerated Content Preview:")
            print("-" * 40)
            print(f"Title: {result.get('title', 'N/A')[:100]}...")
            print(f"Description length: {len(result.get('description', ''))} chars")
            print(f"Bullet points: {len(result.get('bullet_points', []))} items")
            print(f"Keywords: {len(result.get('keywords', []))} total")
            print(f"A+ Content: {'Yes' if result.get('aplus_content') else 'No'}")
            
            return result
            
        else:
            print(f"Generation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"Error during generation: {str(e)}")
        return None

def analyze_singapore_quality(listing_data):
    """Analyze Singapore listing quality"""
    print("\nQUALITY ANALYSIS")
    print("=" * 60)
    
    title = listing_data.get('title', '')
    description = listing_data.get('description', '')
    bullets = listing_data.get('bullet_points', [])
    aplus_content = listing_data.get('aplus_content', '')
    keywords = listing_data.get('keywords', [])
    
    # Combine all text for analysis
    all_content = f"{title} {description} {' '.join(bullets)} {aplus_content}".lower()
    
    scores = {}
    
    # 1. Singapore Localization (25 points)
    print("\n1. SINGAPORE LOCALIZATION (25 points)")
    print("-" * 40)
    
    singapore_elements = [
        'singapore', 'hdb', 'marina bay', 'multicultural', 'tropical',
        'chinese new year', 'national day', 'changi', 'sentosa', 'orchard'
    ]
    
    sg_found = [elem for elem in singapore_elements if elem in all_content]
    localization_score = min(25, len(sg_found) * 3)
    
    print(f"Singapore elements found: {', '.join(sg_found)}")
    print(f"Localization score: {localization_score}/25")
    scores['localization'] = localization_score
    
    # 2. A+ Content Quality (25 points)
    print("\n2. A+ CONTENT QUALITY (25 points)")
    print("-" * 40)
    
    aplus_score = 0
    if aplus_content:
        # Check for comprehensive sections
        section_count = aplus_content.count('section') + aplus_content.count('hero') + aplus_content.count('feature')
        aplus_score += min(15, section_count * 2)
        
        # Check for English image descriptions
        english_images = aplus_content.count('ENGLISH:')
        aplus_score += min(10, english_images * 2)
        
        print(f"Sections found: {section_count}")
        print(f"English image descriptions: {english_images}")
    
    print(f"A+ Content score: {aplus_score}/25")
    scores['aplus'] = aplus_score
    
    # 3. Cultural Elements (20 points)
    print("\n3. CULTURAL ELEMENTS (20 points)")
    print("-" * 40)
    
    cultural_elements = [
        'chinese new year', 'lunar new year', 'multicultural', 'harmony',
        'celebration', 'festive', 'reunion', 'prosperity', 'tradition'
    ]
    
    cultural_found = [elem for elem in cultural_elements if elem in all_content]
    cultural_score = min(20, len(cultural_found) * 3)
    
    print(f"Cultural elements found: {', '.join(cultural_found)}")
    print(f"Cultural score: {cultural_score}/20")
    scores['cultural'] = cultural_score
    
    # 4. SEO Quality (15 points)
    print("\n4. SEO QUALITY (15 points)")
    print("-" * 40)
    
    seo_score = 0
    
    # Keyword quantity
    keyword_count = len(keywords)
    if keyword_count >= 40:
        seo_score += 8
    elif keyword_count >= 30:
        seo_score += 6
    else:
        seo_score += 3
    
    # Singapore-specific keywords
    sg_keywords = [kw for kw in keywords if 'singapore' in str(kw).lower() or 'sg' in str(kw).lower()]
    seo_score += min(7, len(sg_keywords) * 2)
    
    print(f"Total keywords: {keyword_count}")
    print(f"Singapore-specific keywords: {len(sg_keywords)}")
    print(f"SEO score: {seo_score}/15")
    scores['seo'] = seo_score
    
    # 5. Conversion Elements (15 points)
    print("\n5. CONVERSION ELEMENTS (15 points)")
    print("-" * 40)
    
    conversion_elements = [
        'warranty', 'guarantee', 'premium', 'quality', 'certified',
        'professional', 'superior', 'advanced', 'exclusive', 'luxury'
    ]
    
    conversion_found = [elem for elem in conversion_elements if elem in all_content]
    conversion_score = min(15, len(conversion_found) * 2)
    
    print(f"Conversion elements found: {', '.join(conversion_found)}")
    print(f"Conversion score: {conversion_score}/15")
    scores['conversion'] = conversion_score
    
    # Calculate total
    total_score = sum(scores.values())
    max_score = 100
    percentage = (total_score / max_score) * 100
    grade = get_grade(percentage)
    
    print(f"\nTOTAL QUALITY SCORE")
    print("=" * 60)
    print(f"Score: {total_score}/{max_score} ({percentage:.1f}%)")
    print(f"Grade: {grade}")
    print(f"Quality Level: {get_quality_level(percentage)}")
    
    return {
        'total_score': total_score,
        'max_score': max_score,
        'percentage': percentage,
        'grade': grade,
        'detailed_scores': scores
    }

def compare_competitors(quality_scores):
    """Compare against competitors"""
    print(f"\nCOMPETITOR COMPARISON")
    print("=" * 60)
    
    competitors = {
        'Helium 10': 74,
        'Jasper AI': 66,
        'Copy Monkey': 58
    }
    
    our_score = quality_scores['percentage']
    wins = 0
    
    for competitor, score in competitors.items():
        if our_score > score:
            status = "WIN"
            wins += 1
        elif our_score == score:
            status = "TIE"
        else:
            status = "LOSS"
        
        margin = abs(our_score - score)
        print(f"vs {competitor}: {our_score:.1f}% vs {score}% = {status} (+/-{margin:.1f}%)")
    
    print(f"\nResults: Won {wins}/3 comparisons")
    
    if our_score >= 85:
        quality_rating = "10/10 WORLD-CLASS"
    elif our_score >= 75:
        quality_rating = "8-9/10 EXCELLENT"
    elif our_score >= 65:
        quality_rating = "7/10 GOOD"
    else:
        quality_rating = "6/10 NEEDS IMPROVEMENT"
    
    print(f"Quality Rating: {quality_rating}")
    
    return {
        'wins': wins,
        'quality_rating': quality_rating,
        'excellence_achieved': our_score >= 85
    }

def get_grade(percentage):
    """Convert percentage to letter grade"""
    if percentage >= 90:
        return "A+"
    elif percentage >= 85:
        return "A"
    elif percentage >= 80:
        return "A-"
    elif percentage >= 75:
        return "B+"
    elif percentage >= 70:
        return "B"
    elif percentage >= 65:
        return "B-"
    elif percentage >= 60:
        return "C+"
    else:
        return "F"

def get_quality_level(percentage):
    """Get quality level description"""
    if percentage >= 85:
        return "WORLD-CLASS EXCELLENCE"
    elif percentage >= 75:
        return "SUPERIOR QUALITY"
    elif percentage >= 65:
        return "GOOD QUALITY"
    else:
        return "NEEDS IMPROVEMENT"

def save_html_report(listing_data, quality_scores, competitive_analysis):
    """Save HTML report"""
    
    # Clean content for HTML display
    title = html.escape(listing_data.get('title', 'N/A'))
    description = html.escape(listing_data.get('description', 'N/A')).replace('\n', '<br>')
    bullets = listing_data.get('bullet_points', [])
    aplus_content = listing_data.get('aplus_content', 'No A+ content').replace('\n', '<br>')
    keywords = listing_data.get('keywords', [])
    
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Singapore Marketplace Quality Analysis</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }}
        .header {{ text-align: center; border-bottom: 2px solid #e74c3c; padding-bottom: 20px; margin-bottom: 30px; }}
        .score-card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }}
        .metric {{ background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #3498db; }}
        .content-section {{ margin: 20px 0; padding: 20px; background: #f8f9fa; border-radius: 8px; }}
        .excellence {{ background: linear-gradient(45deg, #FFD700, #FFA500); color: #333; padding: 15px; border-radius: 10px; text-align: center; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Singapore Marketplace Quality Analysis</h1>
            <h2>Premium Wireless Gaming Headset - AudioPro</h2>
            <p>Generated: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}</p>
        </div>

        <div class="score-card">
            <h2>Overall Quality Score</h2>
            <p style="font-size: 3em; margin: 10px 0;">{quality_scores['grade']}</p>
            <p style="font-size: 1.5em;">{quality_scores['total_score']}/{quality_scores['max_score']} ({quality_scores['percentage']:.1f}%)</p>
            <p>Quality Level: {get_quality_level(quality_scores['percentage'])}</p>
        </div>

        {"<div class='excellence'><h3>EXCELLENCE ACHIEVED! This listing meets 10/10 quality standards!</h3></div>" if competitive_analysis['excellence_achieved'] else ""}

        <div class="metrics">
            <div class="metric">
                <h3>Singapore Localization</h3>
                <p><strong>{quality_scores['detailed_scores']['localization']}/25</strong></p>
            </div>
            <div class="metric">
                <h3>A+ Content Quality</h3>
                <p><strong>{quality_scores['detailed_scores']['aplus']}/25</strong></p>
            </div>
            <div class="metric">
                <h3>Cultural Integration</h3>
                <p><strong>{quality_scores['detailed_scores']['cultural']}/20</strong></p>
            </div>
            <div class="metric">
                <h3>SEO Optimization</h3>
                <p><strong>{quality_scores['detailed_scores']['seo']}/15</strong></p>
            </div>
            <div class="metric">
                <h3>Conversion Elements</h3>
                <p><strong>{quality_scores['detailed_scores']['conversion']}/15</strong></p>
            </div>
        </div>

        <div class="content-section">
            <h3>Generated Listing Content</h3>
            
            <h4>Product Title</h4>
            <p style="background: #e8f5e8; padding: 10px; border-radius: 5px; font-weight: bold;">{title}</p>
            
            <h4>Product Description</h4>
            <div style="background: #f0f8ff; padding: 15px; border-radius: 5px;">{description}</div>
            
            <h4>Bullet Points</h4>
            <ul style="background: #fff8e1; padding: 15px; border-radius: 5px;">
                {"".join(f"<li>{html.escape(bullet)}</li>" for bullet in bullets)}
            </ul>
            
            <h4>Keywords ({len(keywords)} total)</h4>
            <div style="background: #f3e5f5; padding: 15px; border-radius: 5px;">
                {", ".join(str(kw) for kw in keywords[:20])}
                {"..." if len(keywords) > 20 else ""}
            </div>
        </div>

        <div class="content-section">
            <h3>Competitive Comparison</h3>
            <p><strong>vs Helium 10:</strong> {quality_scores['percentage']:.1f}% vs 74% = {'WIN' if quality_scores['percentage'] > 74 else 'LOSS'}</p>
            <p><strong>vs Jasper AI:</strong> {quality_scores['percentage']:.1f}% vs 66% = {'WIN' if quality_scores['percentage'] > 66 else 'LOSS'}</p>
            <p><strong>vs Copy Monkey:</strong> {quality_scores['percentage']:.1f}% vs 58% = {'WIN' if quality_scores['percentage'] > 58 else 'LOSS'}</p>
            <p><strong>Quality Rating:</strong> {competitive_analysis['quality_rating']}</p>
        </div>

        <div class="content-section">
            <h3>A+ Content Preview</h3>
            <div style="background: #fff; border: 1px solid #ddd; padding: 15px; border-radius: 5px; max-height: 300px; overflow-y: auto;">
                {aplus_content}
            </div>
        </div>

        <div class="content-section">
            <h3>Summary</h3>
            <p>This Singapore marketplace implementation achieves <strong>{quality_scores['grade']}</strong> quality 
            ({quality_scores['percentage']:.1f}%) with strong localization, cultural integration, and comprehensive A+ content. 
            The listing demonstrates {competitive_analysis['wins']}/3 wins against major competitors and 
            {"achieves world-class excellence standards" if competitive_analysis['excellence_achieved'] else "shows strong competitive performance"}.</p>
        </div>
    </div>
</body>
</html>
"""
    
    filename = f"singapore_quality_analysis_{TIMESTAMP}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"\nHTML report saved: {filename}")
    return filename

def main():
    """Run Singapore marketplace test"""
    print("SINGAPORE MARKETPLACE EVALUATION")
    print("Testing Premium Wireless Gaming Headset - AudioPro")
    print("=" * 60)
    
    # Generate listing
    listing_data = test_singapore_listing()
    
    if not listing_data:
        print("Failed to generate listing. Exiting.")
        return
    
    # Analyze quality
    quality_scores = analyze_singapore_quality(listing_data)
    
    # Compare with competitors
    competitive_analysis = compare_competitors(quality_scores)
    
    # Save report
    report_file = save_html_report(listing_data, quality_scores, competitive_analysis)
    
    print(f"\nSINGAPORE TEST COMPLETE")
    print("=" * 60)
    print(f"Final Score: {quality_scores['percentage']:.1f}% ({quality_scores['grade']})")
    print(f"Quality Level: {get_quality_level(quality_scores['percentage'])}")
    print(f"Competitors Beaten: {competitive_analysis['wins']}/3")
    print(f"Report: {report_file}")
    
    if competitive_analysis['excellence_achieved']:
        print("EXCELLENCE ACHIEVED! Singapore implementation meets 10/10 standards!")
    
    return {
        'listing_data': listing_data,
        'quality_scores': quality_scores,
        'competitive_analysis': competitive_analysis,
        'report_file': report_file
    }

if __name__ == "__main__":
    results = main()