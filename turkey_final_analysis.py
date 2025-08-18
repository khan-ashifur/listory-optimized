#!/usr/bin/env python3
"""
Turkey A+ Content Final Analysis Report
"""

import json
import re

def main():
    print("=" * 80)
    print("TURKEY A+ CONTENT FINAL ANALYSIS REPORT")
    print("=" * 80)
    
    # Load the analysis data
    try:
        with open('tr_structure_analysis_20250816_115831.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("ERROR: Analysis file not found. Please run the main test first.")
        return
    
    content = data.get('generated_content', {})
    
    print("\n1. BASIC CONTENT METRICS:")
    print(f"   Title Length: {len(content.get('title', ''))} characters")
    print(f"   Description Length: {len(content.get('description', ''))} characters")
    print(f"   Bullet Points: {len(content.get('bullets', []))}")
    print(f"   Keywords: {len(content.get('keywords', []))}")
    print(f"   A+ Content Length: {len(content.get('aplus_content', ''))} characters")
    
    aplus_content = content.get('aplus_content', '')
    
    print("\n2. SECTION COUNT ANALYSIS:")
    # Count HTML sections
    div_sections = aplus_content.count('<div class="aplus-')
    h3_headers = aplus_content.count('<h3')
    content_blocks = aplus_content.count('content-section')
    
    print(f"   Div Sections: {div_sections}")
    print(f"   H3 Headers: {h3_headers}")
    print(f"   Content Blocks: {content_blocks}")
    print(f"   Total Estimated Sections: {div_sections + h3_headers}")
    
    print("\n3. ENGLISH TITLE VERIFICATION:")
    required_english = ['Keywords', 'Image Strategy', 'SEO Focus', 'Benefits', 'Features', 'Trust', 'Quality']
    found_english = []
    for term in required_english:
        if term in aplus_content:
            found_english.append(term)
            print(f"   FOUND: {term}")
        else:
            print(f"   MISSING: {term}")
    
    compliance_rate = (len(found_english) / len(required_english)) * 100
    print(f"   Compliance Rate: {compliance_rate:.1f}%")
    
    print("\n4. IMAGE DESCRIPTION ANALYSIS:")
    image_descriptions = re.findall(r'showing [^.]{10,100}', aplus_content, re.IGNORECASE)
    english_prefix = re.findall(r'ENGLISH:\s*[A-Za-z]', aplus_content)
    
    print(f"   Image Descriptions Found: {len(image_descriptions)}")
    print(f"   ENGLISH: Prefix Usage: {len(english_prefix)}")
    
    if image_descriptions:
        print("   Sample Descriptions:")
        for i, desc in enumerate(image_descriptions[:3], 1):
            print(f"      {i}. {desc}")
    
    print("\n5. TURKISH LOCALIZATION:")
    full_text = f"{content.get('title', '')} {content.get('description', '')} {aplus_content}"
    
    turkish_chars = ['ç', 'ğ', 'ı', 'ö', 'ş', 'ü', 'Ç', 'Ğ', 'İ', 'Ö', 'Ş', 'Ü']
    turkish_count = sum(full_text.count(char) for char in turkish_chars)
    
    cultural_terms = ['türk', 'türkiye', 'garanti', 'kalite', 'orijinal', 'sertifikalı']
    cultural_found = [term for term in cultural_terms if term in full_text.lower()]
    
    currency_terms = ['₺', 'tl', 'lira']
    currency_found = [term for term in currency_terms if term in full_text.lower()]
    
    print(f"   Turkish Characters: {turkish_count} occurrences")
    print(f"   Cultural Terms: {len(cultural_found)} found - {cultural_found}")
    print(f"   Currency References: {len(currency_found)} found - {currency_found}")
    
    print("\n6. HTML STRUCTURE ANALYSIS:")
    html_tags = ['<div', '<h1', '<h2', '<h3', '<p', '<ul', '<li', '<strong']
    html_count = sum(aplus_content.count(tag) for tag in html_tags)
    
    responsive_classes = ['sm:', 'md:', 'lg:']
    responsive_count = sum(aplus_content.count(cls) for cls in responsive_classes)
    
    print(f"   HTML Elements: {html_count}")
    print(f"   Responsive Classes: {responsive_count}")
    print(f"   Mobile Optimized: {'YES' if responsive_count > 10 else 'NO'}")
    
    print("\n7. CONTENT QUALITY INDICATORS:")
    trust_terms = ['garanti', 'sertifika', 'güven', 'orijinal', 'iade']
    trust_count = sum(1 for term in trust_terms if term in aplus_content.lower())
    
    feature_terms = ['özellik', 'fayda', 'avantaj', 'kalite']
    feature_count = sum(1 for term in feature_terms if term in aplus_content.lower())
    
    print(f"   Trust Indicators: {trust_count}")
    print(f"   Feature References: {feature_count}")
    print(f"   Professional Tone: {'YES' if 'profesyonel' in full_text.lower() else 'NO'}")
    
    print("\n8. FINAL COMPLIANCE ASSESSMENT:")
    
    # Calculate scores
    section_score = 20 if (div_sections + h3_headers) >= 8 else ((div_sections + h3_headers) / 8) * 20
    english_score = (compliance_rate / 100) * 20
    image_score = min(20, len(image_descriptions) * 5)
    localization_score = min(20, (len(cultural_found) * 3) + (len(currency_found) * 2) + (turkish_count // 10))
    quality_score = min(20, (trust_count * 3) + (feature_count * 2) + (html_count // 5))
    
    total_score = section_score + english_score + image_score + localization_score + quality_score
    
    print(f"   Section Count (8+): {section_score:.1f}/20")
    print(f"   English Titles: {english_score:.1f}/20")
    print(f"   Image Descriptions: {image_score:.1f}/20")
    print(f"   Turkish Localization: {localization_score:.1f}/20")
    print(f"   Content Quality: {quality_score:.1f}/20")
    print(f"   TOTAL SCORE: {total_score:.1f}/100")
    
    if total_score >= 90:
        grade = "A+"
    elif total_score >= 80:
        grade = "A"
    elif total_score >= 70:
        grade = "B"
    else:
        grade = "C"
    
    print(f"   GRADE: {grade}")
    print(f"   STATUS: {'MEETS REQUIREMENTS' if total_score >= 80 else 'NEEDS IMPROVEMENT'}")
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    print("STRENGTHS:")
    if div_sections + h3_headers >= 8:
        print("  + Excellent section count (8+ detailed sections)")
    if compliance_rate >= 80:
        print("  + Strong English title compliance")
    if len(cultural_found) >= 4:
        print("  + Excellent Turkish localization")
    if responsive_count > 10:
        print("  + Mobile-responsive design")
    if trust_count >= 3:
        print("  + Strong trust indicators")
    
    print("\nAREAS FOR IMPROVEMENT:")
    if len(image_descriptions) < 3:
        print("  - Need more detailed image descriptions")
    if len(english_prefix) == 0:
        print("  - Missing ENGLISH: prefix in image descriptions")
    if compliance_rate < 80:
        print("  - Some required English section titles missing")
    
    return {
        'total_score': total_score,
        'grade': grade,
        'sections': div_sections + h3_headers,
        'english_compliance': compliance_rate,
        'localization_quality': len(cultural_found) + len(currency_found)
    }

if __name__ == "__main__":
    try:
        result = main()
        print("\nAnalysis completed successfully!")
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()