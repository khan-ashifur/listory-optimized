#!/usr/bin/env python3

"""
Detailed Content Comparison: Turkey vs Mexico A+ Content
Focus: Image strategies, content patterns, and exact text differences
"""

import re

def analyze_image_strategies(html_content, market_name):
    """Extract and analyze image strategy sections"""
    image_strategy_pattern = r'<strong class="text-gray-900">(?:Image Strategy|Görsel Strateji)</strong>\s*</div>\s*<p class="text-gray-600">(.*?)</p>'
    image_strategies = re.findall(image_strategy_pattern, html_content, re.DOTALL)
    
    print(f"\n{market_name} IMAGE STRATEGIES:")
    print("-" * 50)
    
    if not image_strategies:
        print("No image strategies found")
        return []
    
    for i, strategy in enumerate(image_strategies, 1):
        cleaned_strategy = strategy.strip()
        print(f"Strategy {i}: {cleaned_strategy}")
        
        # Check for English content
        english_pattern = r'\bENGLISH:\s*'
        has_english_prefix = bool(re.search(english_pattern, cleaned_strategy, re.IGNORECASE))
        
        if has_english_prefix:
            print(f"  Has 'ENGLISH:' prefix")
        else:
            print(f"  Missing 'ENGLISH:' prefix")
        
        # Check language of content
        if any(word in cleaned_strategy.lower() for word in ['turkish', 'turkey', 'türk']):
            print(f"   Contains Turkish references")
        elif any(word in cleaned_strategy.lower() for word in ['mexican', 'mexico']):
            print(f"   Contains Mexican references")
        
        print(f"   Length: {len(cleaned_strategy)} characters")
        print()
    
    return image_strategies

def analyze_section_headers(html_content, market_name):
    """Extract and analyze section headers"""
    header_pattern = r'<strong class="text-gray-900">(.*?)</strong>'
    headers = re.findall(header_pattern, html_content)
    
    print(f"\n {market_name} SECTION HEADERS:")
    print("-" * 50)
    
    for header in headers:
        print(f"- {header}")
    
    return headers

def analyze_keywords_sections(html_content, market_name):
    """Extract and analyze keyword sections"""
    # Pattern for Keywords/Anahtar Kelimeler sections
    keywords_pattern = r'<strong class="text-gray-900">(?:Keywords|Anahtar Kelimeler)</strong>\s*</div>\s*<p class="text-gray-600">(.*?)</p>'
    keywords_sections = re.findall(keywords_pattern, html_content, re.DOTALL)
    
    print(f"\n {market_name} KEYWORDS SECTIONS:")
    print("-" * 50)
    
    for i, keywords in enumerate(keywords_sections, 1):
        cleaned_keywords = keywords.strip()
        print(f"Section {i}: {cleaned_keywords}")
    
    return keywords_sections

def analyze_seo_focus_sections(html_content, market_name):
    """Extract and analyze SEO Focus sections"""
    seo_pattern = r'<strong class="text-gray-900">(?:SEO Focus|SEO Odak)</strong>\s*</div>\s*<p class="text-gray-600">(.*?)</p>'
    seo_sections = re.findall(seo_pattern, html_content, re.DOTALL)
    
    print(f"\n {market_name} SEO FOCUS SECTIONS:")
    print("-" * 50)
    
    for i, seo in enumerate(seo_sections, 1):
        cleaned_seo = seo.strip()
        if cleaned_seo:
            print(f"Section {i}: {cleaned_seo}")
        else:
            print(f"Section {i}:  EMPTY")
    
    return seo_sections

def compare_markets():
    """Compare Turkey and Mexico A+ content in detail"""
    print("DETAILED TURKEY vs MEXICO A+ CONTENT COMPARISON")
    print("=" * 80)
    
    # Read Mexico content
    try:
        with open('mx_aplus_content_20250816_101329.html', 'r', encoding='utf-8') as f:
            mx_content = f.read()
    except FileNotFoundError:
        print(" Mexico A+ content file not found")
        return
    
    # Read Turkey content  
    try:
        with open('tr_aplus_content_20250816_101418.html', 'r', encoding='utf-8') as f:
            tr_content = f.read()
    except FileNotFoundError:
        print(" Turkey A+ content file not found")
        return
    
    # Analyze Mexico
    print("\n MEXICO ANALYSIS")
    print("=" * 50)
    mx_images = analyze_image_strategies(mx_content, "MEXICO")
    mx_headers = analyze_section_headers(mx_content, "MEXICO")
    mx_keywords = analyze_keywords_sections(mx_content, "MEXICO")
    mx_seo = analyze_seo_focus_sections(mx_content, "MEXICO")
    
    # Analyze Turkey
    print("\n TURKEY ANALYSIS")
    print("=" * 50)
    tr_images = analyze_image_strategies(tr_content, "TURKEY")
    tr_headers = analyze_section_headers(tr_content, "TURKEY")
    tr_keywords = analyze_keywords_sections(tr_content, "TURKEY")
    tr_seo = analyze_seo_focus_sections(tr_content, "TURKEY")
    
    # Compare findings
    print("\n COMPARISON RESULTS")
    print("=" * 80)
    
    print(f"\n1. IMAGE STRATEGIES:")
    print(f"   Mexico strategies: {len(mx_images)}")
    print(f"   Turkey strategies: {len(tr_images)}")
    
    # Check for ENGLISH prefix consistency
    mx_has_english = any('ENGLISH:' in img for img in mx_images)
    tr_has_english = any('ENGLISH:' in img for img in tr_images)
    
    print(f"\n2. ENGLISH PREFIX CONSISTENCY:")
    print(f"   Mexico has 'ENGLISH:' prefix: {mx_has_english}")
    print(f"   Turkey has 'ENGLISH:' prefix: {tr_has_english}")
    
    if mx_has_english and not tr_has_english:
        print("    CRITICAL ISSUE: Turkey missing 'ENGLISH:' prefix in image strategies")
    elif not mx_has_english and tr_has_english:
        print("    CRITICAL ISSUE: Mexico missing 'ENGLISH:' prefix in image strategies")
    elif mx_has_english and tr_has_english:
        print("    Both markets have 'ENGLISH:' prefix")
    else:
        print("    Neither market has 'ENGLISH:' prefix")
    
    print(f"\n3. SECTION HEADERS:")
    mx_english_headers = [h for h in mx_headers if not any(char in h for char in 'I')]
    tr_english_headers = [h for h in tr_headers if not any(char in h for char in 'I')]
    
    print(f"   Mexico English headers: {len(mx_english_headers)}")
    print(f"   Turkey English headers: {len(tr_english_headers)}")
    
    print(f"\n4. SEO FOCUS SECTIONS:")
    mx_empty_seo = sum(1 for seo in mx_seo if not seo.strip())
    tr_empty_seo = sum(1 for seo in tr_seo if not seo.strip())
    
    print(f"   Mexico empty SEO sections: {mx_empty_seo}")
    print(f"   Turkey empty SEO sections: {tr_empty_seo}")
    
    if tr_empty_seo > mx_empty_seo:
        print("    CRITICAL ISSUE: Turkey has more empty SEO sections than Mexico")
    
    # Summary
    print(f"\n CRITICAL ISSUES IDENTIFIED:")
    issues = []
    
    if mx_has_english and not tr_has_english:
        issues.append("Turkey missing 'ENGLISH:' prefix in image strategies")
    
    if tr_empty_seo > mx_empty_seo:
        issues.append("Turkey has empty SEO Focus sections")
    
    if len(tr_english_headers) > len(mx_english_headers):
        issues.append("Turkey has more English headers than Mexico")
    
    if not issues:
        print("    No critical structural issues found")
    else:
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")

if __name__ == "__main__":
    compare_markets()