#!/usr/bin/env python3
"""
Detailed Turkey A+ Content Analysis
Examines the generated A+ content against specific requirements
"""

import json
import re
from bs4 import BeautifulSoup

def analyze_turkey_aplus_content():
    """Detailed analysis of Turkey A+ content"""
    
    print("=" * 80)
    print("TR DETAILED TURKEY A+ CONTENT ANALYSIS")
    print("=" * 80)
    
    # Load the latest analysis data
    try:
        with open('tr_structure_analysis_20250816_115831.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ Analysis file not found. Please run the main test first.")
        return
    
    generated_content = data.get('generated_content', {})
    aplus_content = generated_content.get('aplus_content', '')
    
    print(f"\n📋 CONTENT OVERVIEW:")
    print(f"   📝 Title: {generated_content.get('title', '')[:80]}...")
    print(f"   📊 A+ Content Length: {len(aplus_content):,} characters")
    print(f"   🎯 Bullet Points: {len(generated_content.get('bullets', []))} items")
    print(f"   🔍 Keywords: {len(generated_content.get('keywords', []))} total")
    
    # Parse HTML content
    soup = BeautifulSoup(aplus_content, 'html.parser')
    
    # 1. Section Analysis
    print(f"\n" + "=" * 60)
    print(f"1️⃣ DETAILED SECTION ANALYSIS")
    print(f"=" * 60)
    
    sections = analyze_aplus_sections(soup, aplus_content)
    print(f"   ✅ Total Sections Found: {sections['total_count']}")
    print(f"   📋 Section Types:")
    for section_type, count in sections['types'].items():
        print(f"      • {section_type}: {count}")
    
    # 2. English Title Analysis
    print(f"\n" + "=" * 60)
    print(f"2️⃣ ENGLISH TITLE VERIFICATION")
    print(f"=" * 60)
    
    english_analysis = analyze_english_titles(aplus_content)
    print(f"   🎯 Required English Titles Found:")
    for title in english_analysis['required_titles']:
        status = "✅" if title in english_analysis['found_titles'] else "❌"
        print(f"      {status} {title}")
    
    print(f"   📊 Compliance Rate: {english_analysis['compliance_rate']:.1f}%")
    
    # 3. Image Strategy Analysis
    print(f"\n" + "=" * 60)
    print(f"3️⃣ IMAGE STRATEGY & DESCRIPTIONS")
    print(f"=" * 60)
    
    image_analysis = analyze_image_strategies(aplus_content)
    print(f"   🖼️ Image Strategy Sections: {image_analysis['strategy_sections']}")
    print(f"   📝 Total Image Descriptions: {image_analysis['total_descriptions']}")
    print(f"   🌐 ENGLISH: Prefix Usage: {image_analysis['english_prefix_count']}")
    
    if image_analysis['detailed_descriptions']:
        print(f"   📋 Sample Image Descriptions:")
        for i, desc in enumerate(image_analysis['detailed_descriptions'][:3], 1):
            print(f"      {i}. {desc[:100]}...")
    
    # 4. Turkish Localization Deep Dive
    print(f"\n" + "=" * 60)
    print(f"4️⃣ TURKISH LOCALIZATION DEEP DIVE")
    print(f"=" * 60)
    
    localization = analyze_turkish_localization_detailed(generated_content)
    print(f"   🇹🇷 Turkish Character Usage: {localization['char_percentage']:.1f}%")
    print(f"   🏛️ Cultural Elements Found: {len(localization['cultural_elements'])}")
    print(f"   💰 Currency References: {len(localization['currency_refs'])}")
    print(f"   🎯 Turkish-specific Terms: {len(localization['turkish_terms'])}")
    
    print(f"   📋 Cultural Elements:")
    for element in localization['cultural_elements'][:5]:
        print(f"      • {element}")
    
    # 5. Content Quality Assessment
    print(f"\n" + "=" * 60)
    print(f"5️⃣ CONTENT QUALITY ASSESSMENT")
    print(f"=" * 60)
    
    quality = assess_content_quality(generated_content, aplus_content)
    print(f"   📊 Overall Content Score: {quality['overall_score']}/100")
    print(f"   📝 Content Depth: {quality['depth_score']}/25")
    print(f"   🎨 Visual Integration: {quality['visual_score']}/25")
    print(f"   🌐 Localization Quality: {quality['localization_score']}/25")
    print(f"   🛡️ Trust Indicators: {quality['trust_score']}/25")
    
    # 6. Compliance Summary
    print(f"\n" + "=" * 60)
    print(f"🏆 FINAL COMPLIANCE SUMMARY")
    print(f"=" * 60)
    
    compliance = calculate_final_compliance(sections, english_analysis, image_analysis, localization, quality)
    print(f"   📊 Total Compliance Score: {compliance['total_score']}/100")
    print(f"   🏅 Grade: {compliance['grade']}")
    print(f"   {'✅ MEETS ALL REQUIREMENTS' if compliance['total_score'] >= 80 else '⚠️ NEEDS IMPROVEMENT'}")
    
    print(f"\n   📋 Detailed Breakdown:")
    for category, score in compliance['breakdown'].items():
        status = "✅" if score >= 16 else "⚠️" if score >= 12 else "❌"
        print(f"      {status} {category}: {score}/20")
    
    return compliance

def analyze_aplus_sections(soup, content):
    """Analyze A+ content sections"""
    
    # Find different types of sections
    section_cards = soup.find_all('div', class_=lambda x: x and 'aplus-section-card' in x)
    content_sections = soup.find_all('div', class_=lambda x: x and any(cls in str(x) for cls in ['aplus-', 'bg-', 'border-']))
    
    # Count by types
    types = {
        'Strategy Cards': len(section_cards),
        'Feature Sections': len(soup.find_all(string=re.compile(r'Özellik|Feature', re.I))),
        'Trust Sections': len(soup.find_all(string=re.compile(r'Güven|Trust|Garanti', re.I))),
        'FAQ Sections': len(soup.find_all(string=re.compile(r'Soru|FAQ|Question', re.I))),
        'What\'s in Box': len(soup.find_all(string=re.compile(r'Kutu|Box', re.I))),
        'Hero Sections': len(soup.find_all('div', class_=lambda x: x and 'hero' in str(x))),
        'Quality Sections': len(soup.find_all(string=re.compile(r'Kalite|Quality', re.I)))
    }
    
    total_count = len(content_sections) + len(section_cards)
    
    return {
        'total_count': total_count,
        'types': types,
        'section_cards': len(section_cards)
    }

def analyze_english_titles(content):
    """Analyze English title compliance"""
    
    required_titles = ['Keywords', 'Image Strategy', 'SEO Focus', 'Benefits', 'Features', 'Trust', 'Quality']
    found_titles = []
    
    for title in required_titles:
        if title.lower() in content.lower():
            found_titles.append(title)
    
    compliance_rate = (len(found_titles) / len(required_titles)) * 100
    
    return {
        'required_titles': required_titles,
        'found_titles': found_titles,
        'compliance_rate': compliance_rate
    }

def analyze_image_strategies(content):
    """Analyze image strategy descriptions"""
    
    # Count image strategy sections
    strategy_pattern = r'Image Strategy'
    strategy_sections = len(re.findall(strategy_pattern, content, re.IGNORECASE))
    
    # Find image descriptions
    image_desc_patterns = [
        r'showing [^.]{20,100}',
        r'image showing [^.]{10,80}',
        r'visual [^.]{10,60}',
        r'\d+x\d+px'  # Dimensions
    ]
    
    total_descriptions = 0
    detailed_descriptions = []
    
    for pattern in image_desc_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        total_descriptions += len(matches)
        detailed_descriptions.extend(matches)
    
    # Check for ENGLISH: prefix
    english_prefix_count = len(re.findall(r'ENGLISH:\s*[A-Za-z]', content))
    
    return {
        'strategy_sections': strategy_sections,
        'total_descriptions': total_descriptions,
        'english_prefix_count': english_prefix_count,
        'detailed_descriptions': detailed_descriptions[:5]  # Sample
    }

def analyze_turkish_localization_detailed(content):
    """Detailed Turkish localization analysis"""
    
    # Combine all text content
    all_text = ' '.join([
        content.get('title', ''),
        content.get('description', ''),
        ' '.join(content.get('bullets', [])),
        content.get('aplus_content', '')
    ])
    
    # Turkish characters
    turkish_chars = ['ç', 'ğ', 'ı', 'ö', 'ş', 'ü', 'Ç', 'Ğ', 'İ', 'Ö', 'Ş', 'Ü']
    turkish_char_count = sum(all_text.count(char) for char in turkish_chars)
    char_percentage = (turkish_char_count / len(all_text)) * 100 if all_text else 0
    
    # Cultural elements
    cultural_terms = [
        'türk', 'türkiye', 'misafir', 'misafirperverlik', 'aile', 'bayram',
        'garanti', 'orijinal', 'kalite', 'sertifikalı', 'yerli', 'kargo'
    ]
    
    cultural_elements = []
    for term in cultural_terms:
        if term in all_text.lower():
            cultural_elements.append(term)
    
    # Currency references
    currency_patterns = ['₺', 'tl', 'lira', 'türk lirası']
    currency_refs = []
    for pattern in currency_patterns:
        if pattern in all_text.lower():
            currency_refs.append(pattern)
    
    # Turkish-specific terms
    turkish_specific = [
        'ce sertifikalı', 'tse belgeli', 'türkçe destek', 'türkiye kargo',
        'faturalı satış', 'müşteri desteği', 'iade hakkı'
    ]
    
    turkish_terms = []
    for term in turkish_specific:
        if term in all_text.lower():
            turkish_terms.append(term)
    
    return {
        'char_percentage': char_percentage,
        'cultural_elements': cultural_elements,
        'currency_refs': currency_refs,
        'turkish_terms': turkish_terms
    }

def assess_content_quality(content, aplus_content):
    """Assess overall content quality"""
    
    # Content depth (25 points)
    word_count = len(content.get('description', '').split())
    bullet_quality = len([b for b in content.get('bullets', []) if len(b) > 100])
    depth_score = min(25, (word_count // 10) + (bullet_quality * 3))
    
    # Visual integration (25 points)
    html_elements = ['<div', '<h1', '<h2', '<h3', '<img', '<ul', '<li', '<p']
    visual_elements = sum(1 for elem in html_elements if elem in aplus_content)
    visual_score = min(25, visual_elements * 3)
    
    # Localization quality (25 points)
    turkish_words = ['çeviri', 'kulaklık', 'garanti', 'kalite', 'müşteri', 'ürün']
    localization_count = sum(1 for word in turkish_words if word in aplus_content.lower())
    localization_score = min(25, localization_count * 4)
    
    # Trust indicators (25 points)
    trust_terms = ['garanti', 'sertifika', 'güven', 'orijinal', 'iade', 'destek']
    trust_count = sum(1 for term in trust_terms if term in aplus_content.lower())
    trust_score = min(25, trust_count * 4)
    
    overall_score = depth_score + visual_score + localization_score + trust_score
    
    return {
        'overall_score': overall_score,
        'depth_score': depth_score,
        'visual_score': visual_score,
        'localization_score': localization_score,
        'trust_score': trust_score
    }

def calculate_final_compliance(sections, english_analysis, image_analysis, localization, quality):
    """Calculate final compliance score"""
    
    # Section compliance (20 points)
    section_score = 20 if sections['total_count'] >= 8 else (sections['total_count'] / 8) * 20
    
    # English title compliance (20 points)
    english_score = (english_analysis['compliance_rate'] / 100) * 20
    
    # Image strategy compliance (20 points)
    image_score = min(20, (image_analysis['strategy_sections'] * 5) + (image_analysis['total_descriptions'] * 2))
    
    # Localization compliance (20 points)
    localization_score = min(20, (len(localization['cultural_elements']) * 2) + (len(localization['turkish_terms']) * 3))
    
    # Quality compliance (20 points)
    quality_score = (quality['overall_score'] / 100) * 20
    
    total_score = section_score + english_score + image_score + localization_score + quality_score
    
    # Calculate grade
    if total_score >= 90: grade = "A+"
    elif total_score >= 80: grade = "A"
    elif total_score >= 70: grade = "B"
    elif total_score >= 60: grade = "C"
    else: grade = "F"
    
    return {
        'total_score': round(total_score),
        'grade': grade,
        'breakdown': {
            'Section Count (8+)': round(section_score),
            'English Titles': round(english_score),
            'Image Strategy': round(image_score),
            'Turkish Localization': round(localization_score),
            'Content Quality': round(quality_score)
        }
    }

if __name__ == "__main__":
    try:
        compliance_result = analyze_turkey_aplus_content()
        print(f"\n✅ Detailed analysis completed!")
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()