#!/usr/bin/env python3
"""
Turkey A+ Content Generation and Evaluation Test
Creates comprehensive Amazon listing for Turkey market and evaluates A+ content quality
"""

import os
import sys
import django
import json
import requests
from datetime import datetime
import re

# Add Django project to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

def test_turkey_aplus_generation():
    """Generate Turkey listing and evaluate A+ content quality"""
    
    print("=" * 80)
    print("🇹🇷 TURKEY A+ CONTENT GENERATION & EVALUATION TEST")
    print("=" * 80)
    
    # Test product specifications
    product_data = {
        "name": "Premium AI Translation Earbuds",
        "brand_name": "TechFlow",
        "brand_tone": "professional",
        "target_platform": "amazon",
        "marketplace": "tr",
        "marketplace_language": "tr",
        "description": "Revolutionary AI-powered translation earbuds designed for Turkish business professionals and families. Features real-time translation support for 40 languages with 60-hour battery life for extended use.",
        "target_audience": "Turkish business professionals and families seeking seamless multilingual communication",
        "features": "Real-time translation, 40 languages, 60H battery life, noise cancellation, premium build quality",
        "categories": "Electronics, Audio, Headphones, Translation Devices",
        "price": "299.99",
        "user": 1  # Use existing user or create one
    }
    
    print(f"\n📝 TEST SPECIFICATIONS:")
    print(f"   Product: {product_data['name']}")
    print(f"   Brand: {product_data['brand_name']}")
    print(f"   Categories: {product_data['categories']}")
    print(f"   Target: {product_data['target_audience']}")
    print(f"   Features: {product_data['features']}")
    print(f"   Market: Turkey (tr)")
    print(f"   Platform: {product_data['target_platform']}")
    print(f"   Brand Tone: {product_data['brand_tone']}")
    
    try:
        # Step 1: Create product first
        print(f"\n🔄 Step 1: Creating product...")
        create_url = "http://127.0.0.1:8000/api/core/products/"
        create_response = requests.post(create_url, json=product_data, timeout=60)
        
        if create_response.status_code in [200, 201]:
            product_result = create_response.json()
            product_id = product_result.get('id')
            print(f"✅ Product created with ID: {product_id}")
            
            # Step 2: Generate listing for Turkey market
            print(f"\n🔄 Step 2: Generating Turkey listing...")
            generate_url = f"http://127.0.0.1:8000/api/listings/generate/{product_id}/amazon/"
            generate_data = {"market": "tr", "platform": "amazon"}
            
            generate_response = requests.post(generate_url, json=generate_data, timeout=120)
            
            if generate_response.status_code in [200, 201]:
                result = generate_response.json()
                print(f"✅ Listing generated successfully!")
                
                # Evaluate A+ content
                evaluate_aplus_content(result, product_data)
                
                # Save results
                save_test_results(result, product_data)
                
            else:
                print(f"❌ Listing Generation Error: {generate_response.status_code}")
                print(f"Response: {generate_response.text}")
                
        else:
            print(f"❌ Product Creation Error: {create_response.status_code}")
            print(f"Response: {create_response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection Error: {e}")
        print("Make sure Django server is running at http://127.0.0.1:8000/")

def evaluate_aplus_content(result, product_data):
    """Comprehensive A+ content evaluation"""
    
    print(f"\n" + "=" * 60)
    print(f"📊 A+ CONTENT QUALITY EVALUATION")
    print(f"=" * 60)
    
    aplus_content = result.get('amazon_aplus_content', '')
    
    if not aplus_content:
        print("❌ No A+ content found in response")
        return
    
    # 1. Count sections
    sections_found = count_aplus_sections(aplus_content)
    print(f"\n1️⃣ SECTION COUNT ANALYSIS:")
    print(f"   ✅ Found {sections_found} detailed sections")
    print(f"   {'✅ PASS' if sections_found >= 8 else '❌ FAIL'} - Requirement: 8+ sections")
    
    # 2. Check English titles  
    english_compliance = check_english_titles(aplus_content)
    print(f"\n2️⃣ ENGLISH TITLE COMPLIANCE:")
    print(f"   {'✅ PASS' if english_compliance['compliant'] else '❌ FAIL'} - Section titles in English")
    for title in english_compliance['titles_found']:
        print(f"   📝 Found: {title}")
    
    # 3. Image description analysis
    image_analysis = analyze_image_descriptions(aplus_content)
    print(f"\n3️⃣ IMAGE DESCRIPTION ANALYSIS:")
    print(f"   ✅ Found {image_analysis['total_descriptions']} image descriptions")
    print(f"   {'✅ PASS' if image_analysis['english_prefix_count'] > 0 else '❌ FAIL'} - ENGLISH: prefix usage")
    print(f"   📊 Descriptions with ENGLISH: prefix: {image_analysis['english_prefix_count']}")
    
    # 4. Content localization check
    localization_score = check_turkish_localization(result)
    print(f"\n4️⃣ TURKISH LOCALIZATION ANALYSIS:")
    print(f"   📈 Localization Quality: {localization_score['score']}/10")
    print(f"   🇹🇷 Turkish Characters: {'✅ Found' if localization_score['has_turkish_chars'] else '❌ Missing'}")
    print(f"   🎯 Cultural Elements: {'✅ Found' if localization_score['has_cultural_elements'] else '❌ Missing'}")
    print(f"   💰 Turkish Currency: {'✅ Found' if localization_score['has_turkish_currency'] else '❌ Missing'}")
    
    # 5. A+ content structure analysis
    structure_analysis = analyze_aplus_structure(aplus_content)
    print(f"\n5️⃣ A+ CONTENT STRUCTURE:")
    print(f"   📝 Total Content Length: {structure_analysis['total_length']} characters")
    print(f"   🎨 Rich HTML Elements: {'✅ Found' if structure_analysis['has_rich_html'] else '❌ Missing'}")
    print(f"   🖼️ Image Integration: {'✅ Found' if structure_analysis['has_images'] else '❌ Missing'}")
    print(f"   📱 Mobile-Optimized: {'✅ Yes' if structure_analysis['mobile_optimized'] else '❌ No'}")
    
    # 6. Overall compliance score
    overall_score = calculate_overall_score(sections_found, english_compliance, image_analysis, localization_score, structure_analysis)
    print(f"\n" + "=" * 60)
    print(f"🏆 OVERALL COMPLIANCE SCORE")
    print(f"=" * 60)
    print(f"   📊 Final Score: {overall_score['score']}/100")
    print(f"   🎯 Grade: {overall_score['grade']}")
    print(f"   {'✅ MEETS REQUIREMENTS' if overall_score['score'] >= 80 else '❌ NEEDS IMPROVEMENT'}")
    
    # Show detailed breakdown
    print(f"\n📋 SCORE BREAKDOWN:")
    for category, score in overall_score['breakdown'].items():
        print(f"   {category}: {score}/20")
    
    return overall_score

def count_aplus_sections(aplus_content):
    """Count detailed sections in A+ content"""
    # Look for section patterns
    section_patterns = [
        r'<h[1-6][^>]*>.*?</h[1-6]>',  # HTML headers
        r'(?i)(Keywords|Image Strategy|SEO Focus|Benefits|Features|Specifications|Guarantee|Trust|Quality|Why Choose)',
        r'<div[^>]*class[^>]*section[^>]*>',
        r'## .+',  # Markdown headers
    ]
    
    sections_found = 0
    for pattern in section_patterns:
        matches = re.findall(pattern, aplus_content, re.IGNORECASE | re.DOTALL)
        sections_found += len(matches)
    
    # Remove duplicates by looking for unique content blocks
    unique_sections = set()
    lines = aplus_content.split('\n')
    for line in lines:
        if any(word in line.lower() for word in ['keywords', 'image', 'seo', 'benefits', 'features', 'guarantee', 'trust', 'quality']):
            unique_sections.add(line.strip()[:50])  # First 50 chars as identifier
    
    return max(sections_found, len(unique_sections))

def check_english_titles(aplus_content):
    """Check if section titles are in English"""
    english_keywords = ['Keywords', 'Image Strategy', 'SEO Focus', 'Benefits', 'Features', 'Specifications', 'Trust', 'Quality']
    titles_found = []
    compliant_count = 0
    
    for keyword in english_keywords:
        if keyword.lower() in aplus_content.lower():
            titles_found.append(keyword)
            compliant_count += 1
    
    return {
        'compliant': compliant_count >= 3,  # At least 3 English section titles
        'titles_found': titles_found,
        'count': compliant_count
    }

def analyze_image_descriptions(aplus_content):
    """Analyze image descriptions for ENGLISH: prefix and detail"""
    english_prefix_pattern = r'ENGLISH:\s*[A-Za-z]+'
    image_desc_pattern = r'(?i)(image|photo|picture|visual).*?description'
    
    english_prefix_matches = re.findall(english_prefix_pattern, aplus_content)
    image_desc_matches = re.findall(image_desc_pattern, aplus_content)
    
    return {
        'total_descriptions': len(image_desc_matches),
        'english_prefix_count': len(english_prefix_matches),
        'detailed_descriptions': len([m for m in english_prefix_matches if len(m) > 30])
    }

def check_turkish_localization(result):
    """Check quality of Turkish localization"""
    turkish_chars = ['ç', 'ğ', 'ı', 'ö', 'ş', 'ü', 'Ç', 'Ğ', 'İ', 'Ö', 'Ş', 'Ü']
    cultural_indicators = ['türk', 'türkiye', 'garanti', 'kalite', 'orijinal', 'sertifikalı']
    currency_indicators = ['₺', 'tl', 'lira']
    
    # Check title and description
    title = result.get('title', '')
    description = result.get('long_description', '')
    bullets = result.get('bullet_points', '')
    
    full_text = f"{title} {description} {bullets}".lower()
    
    has_turkish_chars = any(char in full_text for char in turkish_chars)
    has_cultural_elements = any(word in full_text for word in cultural_indicators)
    has_turkish_currency = any(currency in full_text for currency in currency_indicators)
    
    # Calculate score
    score = 0
    if has_turkish_chars: score += 4
    if has_cultural_elements: score += 3
    if has_turkish_currency: score += 3
    
    return {
        'score': score,
        'has_turkish_chars': has_turkish_chars,
        'has_cultural_elements': has_cultural_elements,
        'has_turkish_currency': has_turkish_currency
    }

def analyze_aplus_structure(aplus_content):
    """Analyze A+ content structure and formatting"""
    html_elements = ['<div', '<h1', '<h2', '<h3', '<img', '<p', '<ul', '<li']
    rich_html = sum(1 for element in html_elements if element in aplus_content)
    
    return {
        'total_length': len(aplus_content),
        'has_rich_html': rich_html >= 5,
        'has_images': 'img' in aplus_content.lower() or 'image' in aplus_content.lower(),
        'mobile_optimized': 'responsive' in aplus_content.lower() or 'mobile' in aplus_content.lower()
    }

def calculate_overall_score(sections_found, english_compliance, image_analysis, localization_score, structure_analysis):
    """Calculate overall compliance score"""
    
    # Section score (20 points)
    section_score = min(20, (sections_found / 8) * 20)
    
    # English title score (20 points) 
    english_score = 20 if english_compliance['compliant'] else 10
    
    # Image description score (20 points)
    image_score = min(20, image_analysis['english_prefix_count'] * 5)
    
    # Localization score (20 points)
    localization_score_points = (localization_score['score'] / 10) * 20
    
    # Structure score (20 points)
    structure_score = 0
    if structure_analysis['has_rich_html']: structure_score += 8
    if structure_analysis['has_images']: structure_score += 6  
    if structure_analysis['mobile_optimized']: structure_score += 6
    
    total_score = section_score + english_score + image_score + localization_score_points + structure_score
    
    # Grade calculation
    if total_score >= 90: grade = "A+"
    elif total_score >= 80: grade = "A"
    elif total_score >= 70: grade = "B"
    elif total_score >= 60: grade = "C"
    else: grade = "F"
    
    return {
        'score': round(total_score),
        'grade': grade,
        'breakdown': {
            'Sections (8+)': round(section_score),
            'English Titles': round(english_score),
            'Image Descriptions': round(image_score),
            'Turkish Localization': round(localization_score_points),
            'Structure & HTML': round(structure_score)
        }
    }

def save_test_results(result, product_data):
    """Save test results to files"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save A+ content as HTML
    aplus_content = result.get('amazon_aplus_content', '')
    html_filename = f"tr_aplus_content_{timestamp}.html"
    with open(html_filename, 'w', encoding='utf-8') as f:
        f.write(f"""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Turkey A+ Content - {product_data['name']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #232f3e; color: white; padding: 20px; margin-bottom: 20px; }}
        .content {{ line-height: 1.6; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🇹🇷 Turkey A+ Content Analysis</h1>
        <p>Product: {product_data['name']} | Brand: {product_data['brand_name']} | Generated: {timestamp}</p>
    </div>
    <div class="content">
        {aplus_content}
    </div>
</body>
</html>
        """)
    
    # Save detailed analysis as JSON
    analysis_data = {
        'test_info': {
            'timestamp': timestamp,
            'product': product_data,
            'market': 'Turkey (tr)'
        },
        'generated_content': {
            'title': result.get('title', ''),
            'description': result.get('long_description', ''),
            'bullets': result.get('bullet_points', '').split('\n\n') if result.get('bullet_points') else [],
            'aplus_content': aplus_content,
            'keywords': result.get('keywords', '').split(', ') if result.get('keywords') else []
        },
        'evaluation_results': evaluate_aplus_content(result, product_data) if aplus_content else None
    }
    
    json_filename = f"tr_structure_analysis_{timestamp}.json"
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(analysis_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 RESULTS SAVED:")
    print(f"   📄 HTML Preview: {html_filename}")
    print(f"   📊 Analysis Data: {json_filename}")

def main():
    """Main test execution"""
    print("\n🚀 Starting Turkey A+ Content Generation Test...")
    test_turkey_aplus_generation()
    print(f"\n✅ Test completed successfully!")

if __name__ == "__main__":
    main()