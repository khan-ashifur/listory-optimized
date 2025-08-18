#!/usr/bin/env python3

"""
Turkey vs Mexico A+ Content DESIGN STRUCTURE Comparison Test
Focus: HTML structure, CSS classes, module layouts, and visual design elements
Goal: Ensure Turkey has IDENTICAL design structure as Mexico, just with Turkish text
"""

import os
import sys
import django
import json
import re
from datetime import datetime

# Django setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from django.contrib.auth.models import User

def extract_html_structure(html_content):
    """Extract HTML structure, CSS classes, and design elements"""
    if not html_content:
        return {}
    
    structure = {
        'total_length': len(html_content),
        'div_classes': [],
        'section_structures': [],
        'image_elements': [],
        'text_styling': [],
        'module_layouts': [],
        'color_schemes': [],
        'spacing_elements': []
    }
    
    # Extract div classes
    div_matches = re.findall(r'<div[^>]*class="([^"]*)"', html_content, re.IGNORECASE)
    structure['div_classes'] = list(set(div_matches))
    
    # Extract section structures
    section_matches = re.findall(r'<section[^>]*>(.*?)</section>', html_content, re.DOTALL | re.IGNORECASE)
    for i, section in enumerate(section_matches):
        section_info = {
            'index': i,
            'length': len(section),
            'has_image': 'img' in section.lower(),
            'has_heading': any(tag in section.lower() for tag in ['<h1', '<h2', '<h3', '<h4']),
            'div_count': section.lower().count('<div')
        }
        structure['section_structures'].append(section_info)
    
    # Extract image elements
    img_matches = re.findall(r'<img[^>]*>', html_content, re.IGNORECASE)
    structure['image_elements'] = img_matches
    
    # Extract text styling classes
    style_matches = re.findall(r'class="([^"]*(?:text|font|color)[^"]*)"', html_content, re.IGNORECASE)
    structure['text_styling'] = list(set(style_matches))
    
    # Extract module layout patterns
    module_patterns = re.findall(r'<div[^>]*(?:module|section|card|container)[^>]*>', html_content, re.IGNORECASE)
    structure['module_layouts'] = module_patterns
    
    # Extract color and spacing information
    color_matches = re.findall(r'class="[^"]*(?:bg-|text-|border-)[^"]*"', html_content, re.IGNORECASE)
    structure['color_schemes'] = list(set(color_matches))
    
    spacing_matches = re.findall(r'class="[^"]*(?:p-|m-|px-|py-|mx-|my-|space-)[^"]*"', html_content, re.IGNORECASE)
    structure['spacing_elements'] = list(set(spacing_matches))
    
    return structure

def compare_structures(turkey_structure, mexico_structure):
    """Compare HTML structures and identify differences"""
    differences = {
        'critical_differences': [],
        'minor_differences': [],
        'identical_elements': []
    }
    
    # Compare div classes
    turkey_classes = set(turkey_structure.get('div_classes', []))
    mexico_classes = set(mexico_structure.get('div_classes', []))
    
    if turkey_classes != mexico_classes:
        only_turkey = turkey_classes - mexico_classes
        only_mexico = mexico_classes - turkey_classes
        
        if only_turkey or only_mexico:
            differences['critical_differences'].append({
                'type': 'div_classes',
                'turkey_only': list(only_turkey),
                'mexico_only': list(only_mexico)
            })
    else:
        differences['identical_elements'].append('div_classes')
    
    # Compare section structures
    turkey_sections = turkey_structure.get('section_structures', [])
    mexico_sections = mexico_structure.get('section_structures', [])
    
    if len(turkey_sections) != len(mexico_sections):
        differences['critical_differences'].append({
            'type': 'section_count',
            'turkey_count': len(turkey_sections),
            'mexico_count': len(mexico_sections)
        })
    
    # Compare module layouts
    turkey_modules = turkey_structure.get('module_layouts', [])
    mexico_modules = mexico_structure.get('module_layouts', [])
    
    if turkey_modules != mexico_modules:
        differences['critical_differences'].append({
            'type': 'module_layouts',
            'turkey_modules': turkey_modules[:5],  # First 5 for brevity
            'mexico_modules': mexico_modules[:5]
        })
    else:
        differences['identical_elements'].append('module_layouts')
    
    # Compare color schemes
    turkey_colors = set(turkey_structure.get('color_schemes', []))
    mexico_colors = set(mexico_structure.get('color_schemes', []))
    
    if turkey_colors != mexico_colors:
        differences['minor_differences'].append({
            'type': 'color_schemes',
            'turkey_only': list(turkey_colors - mexico_colors),
            'mexico_only': list(mexico_colors - turkey_colors)
        })
    else:
        differences['identical_elements'].append('color_schemes')
    
    # Compare spacing elements
    turkey_spacing = set(turkey_structure.get('spacing_elements', []))
    mexico_spacing = set(mexico_structure.get('spacing_elements', []))
    
    if turkey_spacing != mexico_spacing:
        differences['minor_differences'].append({
            'type': 'spacing_elements',
            'turkey_only': list(turkey_spacing - mexico_spacing),
            'mexico_only': list(mexico_spacing - turkey_spacing)
        })
    else:
        differences['identical_elements'].append('spacing_elements')
    
    return differences

def test_turkey_mexico_aplus_design():
    """Generate listings for Turkey and Mexico and compare A+ design structures"""
    print("🇹🇷 vs 🇲🇽 TURKEY vs MEXICO A+ CONTENT DESIGN STRUCTURE COMPARISON")
    print("=" * 80)
    print("Focus: HTML structure, CSS classes, module layouts, visual design")
    print("=" * 80)
    
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username='turkey_mexico_design_test')
    
    # Test product data
    product_data = {
        'brand_name': "Sensei Tech",
        'description': "Advanced wireless noise-canceling headphones with AI translation technology supporting 40+ languages. Premium sound quality with ergonomic design.",
        'price': 299.99,
        'categories': "Electronics/Audio/Headphones",
        'occasion': "general"
    }
    
    results = {}
    
    # Test markets with specific product names
    markets = [
        {
            'code': 'mx',
            'name': 'Mexico',
            'flag': '🇲🇽',
            'product_name': 'Audífonos Traductores Sensei AI'
        },
        {
            'code': 'tr', 
            'name': 'Turkey',
            'flag': '🇹🇷',
            'product_name': 'Sensei AI Çeviri Kulaklık'
        }
    ]
    
    for market in markets:
        print(f"\n{market['flag']} GENERATING {market['name'].upper()} LISTING")
        print("-" * 60)
        
        # Create product for this market
        product = Product.objects.create(
            user=test_user,
            name=market['product_name'],
            marketplace=market['code'],
            marketplace_language=market['code'],
            **product_data
        )
        
        try:
            result = service.generate_listing(product_id=product.id, platform='amazon')
            
            if result and result.amazon_aplus_content:
                aplus_content = result.amazon_aplus_content
                
                # Extract HTML structure
                structure = extract_html_structure(aplus_content)
                
                # Save full content for detailed analysis
                filename = f"{market['code']}_aplus_content_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(aplus_content)
                
                # Save structure analysis
                structure_filename = f"{market['code']}_structure_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(structure_filename, 'w', encoding='utf-8') as f:
                    json.dump(structure, f, indent=2, ensure_ascii=False)
                
                results[market['code']] = {
                    'content': aplus_content,
                    'structure': structure,
                    'files': {
                        'html': filename,
                        'structure': structure_filename
                    }
                }
                
                print(f"✅ Generated A+ content: {len(aplus_content)} characters")
                print(f"✅ Extracted {len(structure['div_classes'])} unique div classes")
                print(f"✅ Found {len(structure['section_structures'])} sections")
                print(f"✅ Identified {len(structure['module_layouts'])} module layouts")
                print(f"✅ Saved to: {filename}")
                print(f"✅ Structure analysis: {structure_filename}")
                
                # Show key structure elements
                print(f"\n📋 KEY STRUCTURE ELEMENTS:")
                print(f"   - Total div classes: {len(structure['div_classes'])}")
                print(f"   - Section count: {len(structure['section_structures'])}")
                print(f"   - Image elements: {len(structure['image_elements'])}")
                print(f"   - Color classes: {len(structure['color_schemes'])}")
                print(f"   - Spacing classes: {len(structure['spacing_elements'])}")
                
                # Show sample classes
                if structure['div_classes']:
                    print(f"\n🎨 SAMPLE DIV CLASSES:")
                    for cls in structure['div_classes'][:5]:
                        print(f"   - {cls}")
                
            else:
                print(f"❌ Failed to generate A+ content")
                results[market['code']] = {'error': 'No content generated'}
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            results[market['code']] = {'error': str(e)}
        
        # Cleanup
        product.delete()
    
    # Compare structures
    if 'tr' in results and 'mx' in results and 'structure' in results['tr'] and 'structure' in results['mx']:
        print(f"\n🔍 DETAILED STRUCTURE COMPARISON")
        print("=" * 80)
        
        differences = compare_structures(results['tr']['structure'], results['mx']['structure'])
        
        print(f"\n✅ IDENTICAL ELEMENTS:")
        for element in differences['identical_elements']:
            print(f"   - {element}")
        
        if differences['critical_differences']:
            print(f"\n❌ CRITICAL DIFFERENCES (MUST FIX):")
            for diff in differences['critical_differences']:
                print(f"   - {diff['type']}:")
                if 'turkey_only' in diff:
                    print(f"     Turkey only: {diff['turkey_only']}")
                if 'mexico_only' in diff:
                    print(f"     Mexico only: {diff['mexico_only']}")
                if 'turkey_count' in diff:
                    print(f"     Turkey sections: {diff['turkey_count']}")
                    print(f"     Mexico sections: {diff['mexico_count']}")
        
        if differences['minor_differences']:
            print(f"\n⚠️ MINOR DIFFERENCES:")
            for diff in differences['minor_differences']:
                print(f"   - {diff['type']}:")
                if 'turkey_only' in diff:
                    print(f"     Turkey only: {diff['turkey_only'][:3]}")  # Show first 3
                if 'mexico_only' in diff:
                    print(f"     Mexico only: {diff['mexico_only'][:3]}")
        
        # Save comparison results
        comparison_filename = f"turkey_mexico_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        comparison_data = {
            'timestamp': datetime.now().isoformat(),
            'turkey_structure': results['tr']['structure'],
            'mexico_structure': results['mx']['structure'],
            'differences': differences
        }
        
        with open(comparison_filename, 'w', encoding='utf-8') as f:
            json.dump(comparison_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 FULL COMPARISON SAVED TO: {comparison_filename}")
        
        # Determine if design structures match
        critical_count = len(differences['critical_differences'])
        if critical_count == 0:
            print(f"\n🎉 SUCCESS: Turkey and Mexico have IDENTICAL design structures!")
        else:
            print(f"\n⚠️ ISSUE: Found {critical_count} critical design differences")
            print(f"   Turkey A+ design structure needs alignment with Mexico")
    
    else:
        print(f"\n❌ Could not compare structures - missing data")
    
    return results

if __name__ == "__main__":
    test_turkey_mexico_aplus_design()