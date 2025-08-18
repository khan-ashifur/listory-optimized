#!/usr/bin/env python3

"""
Simple Turkey vs Mexico A+ Content Comparison
Extract key differences in image strategies and content patterns
"""

import re

def extract_image_strategies(html_content):
    """Extract image strategy sections"""
    pattern = r'<strong class="text-gray-900">(?:Image Strategy|Görsel Strateji)</strong>\s*</div>\s*<p class="text-gray-600">(.*?)</p>'
    strategies = re.findall(pattern, html_content, re.DOTALL)
    return [s.strip() for s in strategies]

def extract_seo_focus(html_content):
    """Extract SEO Focus sections"""
    pattern = r'<strong class="text-gray-900">(?:SEO Focus|SEO Odak)</strong>\s*</div>\s*<p class="text-gray-600">(.*?)</p>'
    seo_sections = re.findall(pattern, html_content, re.DOTALL)
    return [s.strip() for s in seo_sections]

def analyze_differences():
    """Analyze key differences between Turkey and Mexico"""
    print("TURKEY vs MEXICO A+ CONTENT CRITICAL DIFFERENCES")
    print("=" * 60)
    
    # Read files
    try:
        with open('mx_aplus_content_20250816_101329.html', 'r', encoding='utf-8') as f:
            mx_content = f.read()
        with open('tr_aplus_content_20250816_101418.html', 'r', encoding='utf-8') as f:
            tr_content = f.read()
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return
    
    # Extract image strategies
    mx_images = extract_image_strategies(mx_content)
    tr_images = extract_image_strategies(tr_content)
    
    # Extract SEO focus sections
    mx_seo = extract_seo_focus(mx_content)
    tr_seo = extract_seo_focus(tr_content)
    
    print(f"\n1. IMAGE STRATEGY COUNT:")
    print(f"   Mexico: {len(mx_images)} strategies")
    print(f"   Turkey: {len(tr_images)} strategies")
    
    print(f"\n2. ENGLISH PREFIX ANALYSIS:")
    mx_english_count = sum(1 for img in mx_images if 'ENGLISH:' in img)
    tr_english_count = sum(1 for img in tr_images if 'ENGLISH:' in img)
    
    print(f"   Mexico with 'ENGLISH:' prefix: {mx_english_count}/{len(mx_images)}")
    print(f"   Turkey with 'ENGLISH:' prefix: {tr_english_count}/{len(tr_images)}")
    
    if mx_english_count > tr_english_count:
        print(f"   CRITICAL ISSUE: Turkey missing {mx_english_count - tr_english_count} 'ENGLISH:' prefixes")
    
    print(f"\n3. SAMPLE IMAGE STRATEGIES:")
    print(f"\n   MEXICO (first 2):")
    for i, img in enumerate(mx_images[:2], 1):
        print(f"   {i}. {img[:80]}...")
    
    print(f"\n   TURKEY (first 2):")
    for i, img in enumerate(tr_images[:2], 1):
        print(f"   {i}. {img[:80]}...")
    
    print(f"\n4. SEO FOCUS SECTIONS:")
    mx_empty_seo = sum(1 for seo in mx_seo if not seo)
    tr_empty_seo = sum(1 for seo in tr_seo if not seo)
    
    print(f"   Mexico empty SEO sections: {mx_empty_seo}/{len(mx_seo)}")
    print(f"   Turkey empty SEO sections: {tr_empty_seo}/{len(tr_seo)}")
    
    if tr_empty_seo > mx_empty_seo:
        print(f"   CRITICAL ISSUE: Turkey has {tr_empty_seo - mx_empty_seo} more empty SEO sections")
    
    print(f"\n5. KEY DIFFERENCES IDENTIFIED:")
    issues = []
    
    if mx_english_count > tr_english_count:
        issues.append(f"Turkey missing {mx_english_count - tr_english_count} 'ENGLISH:' prefixes in image strategies")
    
    if tr_empty_seo > mx_empty_seo:
        issues.append(f"Turkey has {tr_empty_seo - mx_empty_seo} more empty SEO sections")
    
    # Check for content length differences
    avg_mx_length = sum(len(img) for img in mx_images) / len(mx_images) if mx_images else 0
    avg_tr_length = sum(len(img) for img in tr_images) / len(tr_images) if tr_images else 0
    
    if abs(avg_mx_length - avg_tr_length) > 20:
        issues.append(f"Image strategy length difference: MX avg {avg_mx_length:.0f} vs TR avg {avg_tr_length:.0f}")
    
    if not issues:
        print("   No critical structural issues found")
    else:
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
    
    return {
        'mx_images': mx_images,
        'tr_images': tr_images,
        'mx_seo': mx_seo,
        'tr_seo': tr_seo,
        'issues': issues
    }

if __name__ == "__main__":
    result = analyze_differences()