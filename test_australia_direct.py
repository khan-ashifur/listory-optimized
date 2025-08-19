#!/usr/bin/env python3
"""
Direct Australia listing test - fetch latest listing and analyze
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

def fetch_latest_listing():
    """Fetch the latest generated listing"""
    try:
        response = requests.get(f"{BASE_URL}/api/listings/generated/")
        if response.status_code == 200:
            listings = response.json()
            if listings and 'results' in listings and listings['results']:
                latest_listing = listings['results'][0]  # First one should be latest
                print(f"Found latest listing: ID {latest_listing.get('id', 'Unknown')}")
                return latest_listing
            else:
                print("No listings found")
                return None
        else:
            print(f"Failed to fetch listings: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching listings: {str(e)}")
        return None

def analyze_australia_listing(listing_data):
    """Quick analysis of Australia listing"""
    print("\n=== AUSTRALIA LISTING ANALYSIS ===")
    
    # Basic info
    print(f"Listing ID: {listing_data.get('id', 'N/A')}")
    print(f"Title: {listing_data.get('product_title', 'N/A')}")
    print(f"Platform: {listing_data.get('platform', 'N/A')}")
    
    # Check for key content
    title = listing_data.get('product_title', '')
    description = listing_data.get('description', '')
    bullets = listing_data.get('bullet_points', [])
    aplus = listing_data.get('a_plus_content', '')
    
    print(f"\nContent Analysis:")
    print(f"Title length: {len(title)} chars")
    print(f"Description length: {len(description)} chars")
    print(f"Bullet points: {len(bullets) if isinstance(bullets, list) else 'N/A'}")
    print(f"A+ content length: {len(aplus)} chars")
    
    # Cultural elements check
    all_text = f"{title} {description} {' '.join(bullets) if isinstance(bullets, list) else ''} {aplus}".lower()
    
    cultural_elements = {
        'australia': all_text.count('australia'),
        'aussie': all_text.count('aussie'),
        'fair dinkum': all_text.count('fair dinkum'),
        'mateship': all_text.count('mateship'),
        'mate': all_text.count('mate'),
        'bbq': all_text.count('bbq'),
        'outback': all_text.count('outback'),
        'sydney': all_text.count('sydney'),
        'melbourne': all_text.count('melbourne')
    }
    
    print(f"\nCultural Elements Found:")
    total_cultural = 0
    for element, count in cultural_elements.items():
        if count > 0:
            print(f"  {element}: {count}")
            total_cultural += count
    
    print(f"Total cultural references: {total_cultural}")
    
    # A+ content analysis
    if aplus:
        print(f"\nA+ Content Analysis:")
        sections = ['hero', 'features', 'comparison', 'lifestyle', 'trust', 'specifications', 'faq', 'guarantee']
        found_sections = [s for s in sections if s in aplus.lower()]
        print(f"Sections found: {found_sections}")
        print(f"ENGLISH descriptions: {aplus.count('ENGLISH:')}")
        
        # Check for Australian context in A+ content
        aus_contexts = ['australian', 'sydney', 'melbourne', 'queensland', 'bondi', 'harbour bridge']
        aus_context_count = sum(aplus.lower().count(ctx) for ctx in aus_contexts)
        print(f"Australian context references: {aus_context_count}")
    
    # Quality assessment
    quality_score = 0
    if len(title) > 50:
        quality_score += 1
    if len(description) > 500:
        quality_score += 1
    if isinstance(bullets, list) and len(bullets) >= 5:
        quality_score += 1
    if len(aplus) > 1000:
        quality_score += 2
    if total_cultural > 0:
        quality_score += 3
    if 'australia' in all_text:
        quality_score += 2
    
    print(f"\nQuick Quality Score: {quality_score}/10")
    grade = "A" if quality_score >= 8 else "B" if quality_score >= 6 else "C" if quality_score >= 4 else "D"
    print(f"Grade: {grade}")
    
    return {
        'title': title,
        'description': description,
        'bullets': bullets,
        'aplus': aplus,
        'cultural_elements': cultural_elements,
        'total_cultural': total_cultural,
        'quality_score': quality_score,
        'grade': grade
    }

def save_analysis(listing_data, analysis):
    """Save analysis to HTML file"""
    html_content = f"""
<!DOCTYPE html>
<html lang="en-au">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Australia Listing Analysis - {TIMESTAMP}</title>
    <style>
        body {{
            font-family: 'Segoe UI', sans-serif;
            margin: 20px;
            background: #f8f9fa;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }}
        .section {{
            margin: 20px 0;
            padding: 20px;
            border-left: 4px solid #FF6B35;
            background: #f8f9fa;
        }}
        .score {{
            font-size: 2em;
            font-weight: bold;
            color: #FF6B35;
        }}
        .grade-a {{ color: #00C851; }}
        .grade-b {{ color: #33B5E5; }}
        .grade-c {{ color: #FF8800; }}
        .grade-d {{ color: #FF4444; }}
        .cultural-tag {{
            display: inline-block;
            background: #FF6B35;
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            margin: 5px;
            font-size: 0.9em;
        }}
        pre {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            white-space: pre-wrap;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Australia Marketplace Listing Analysis</h1>
            <h2>Premium Wireless Gaming Headset Pro</h2>
            <div class="score grade-{analysis['grade'].lower()}">{analysis['quality_score']}/10 ({analysis['grade']})</div>
        </div>
        
        <div class="section">
            <h2>Product Title</h2>
            <p><strong>{analysis['title']}</strong></p>
            <p>Length: {len(analysis['title'])} characters</p>
        </div>
        
        <div class="section">
            <h2>Product Description</h2>
            <pre>{analysis['description']}</pre>
            <p>Length: {len(analysis['description'])} characters</p>
        </div>
        
        <div class="section">
            <h2>Bullet Points</h2>
            <ul>
    """
    
    if isinstance(analysis['bullets'], list):
        for bullet in analysis['bullets']:
            html_content += f"<li>{bullet}</li>"
    else:
        html_content += "<li>No bullet points found</li>"
    
    html_content += f"""
            </ul>
            <p>Count: {len(analysis['bullets']) if isinstance(analysis['bullets'], list) else 0}</p>
        </div>
        
        <div class="section">
            <h2>Cultural Integration</h2>
            <p><strong>Total Cultural References: {analysis['total_cultural']}</strong></p>
            <div>
    """
    
    for element, count in analysis['cultural_elements'].items():
        if count > 0:
            html_content += f'<span class="cultural-tag">{element}: {count}</span>'
    
    html_content += f"""
            </div>
        </div>
        
        <div class="section">
            <h2>A+ Content</h2>
            <p>Length: {len(analysis['aplus'])} characters</p>
            <pre>{analysis['aplus'][:2000]}{'...' if len(analysis['aplus']) > 2000 else ''}</pre>
        </div>
        
        <div class="section">
            <h2>Quality Assessment</h2>
            <p><strong>Score: {analysis['quality_score']}/10</strong></p>
            <p><strong>Grade: {analysis['grade']}</strong></p>
            <p>Analysis completed on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>
    </div>
</body>
</html>
    """
    
    filename = f"australia_listing_analysis_{TIMESTAMP}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\nAnalysis saved to: {filename}")
    return filename

if __name__ == "__main__":
    print("AUSTRALIA LISTING DIRECT ANALYSIS")
    print("=" * 50)
    
    listing = fetch_latest_listing()
    if listing:
        analysis = analyze_australia_listing(listing)
        save_analysis(listing, analysis)
        
        print("\n" + "=" * 50)
        print("ANALYSIS COMPLETE!")
        print("=" * 50)
    else:
        print("No listing found to analyze")