#!/usr/bin/env python3
"""
Fetch Australia listing content directly
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def fetch_listing_detail(listing_id):
    """Fetch detailed listing content"""
    try:
        response = requests.get(f"{BASE_URL}/api/listings/generated/{listing_id}/")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch listing {listing_id}: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def display_listing_content(listing):
    """Display listing content in readable format"""
    print("=" * 80)
    print("AUSTRALIA LISTING CONTENT ANALYSIS")
    print("=" * 80)
    
    # Basic info
    print(f"Listing ID: {listing.get('id', 'N/A')}")
    print(f"Platform: {listing.get('platform', 'N/A')}")
    print(f"Status: {listing.get('status', 'N/A')}")
    print(f"Created: {listing.get('created_at', 'N/A')}")
    
    # Title
    title = listing.get('title', '')
    print(f"\nTITLE ({len(title)} chars):")
    print(f"'{title}'")
    
    # Description (try both long_description and short_description)
    description = listing.get('long_description', listing.get('short_description', ''))
    print(f"\nDESCRIPTION ({len(description)} chars):")
    print(description)
    
    # Bullet Points
    bullets_raw = listing.get('bullet_points', '')
    if bullets_raw:
        # Try to parse if it's a string representation of a list
        if bullets_raw.startswith('[') and bullets_raw.endswith(']'):
            try:
                import ast
                bullets = ast.literal_eval(bullets_raw)
            except:
                bullets = bullets_raw.split('\n') if '\n' in bullets_raw else [bullets_raw]
        else:
            bullets = bullets_raw.split('\n') if '\n' in bullets_raw else [bullets_raw]
    else:
        bullets = []
    
    print(f"\nBULLET POINTS ({len(bullets) if bullets else 'N/A'}):")
    if bullets:
        for i, bullet in enumerate(bullets, 1):
            if bullet.strip():  # Skip empty lines
                print(f"{i}. {bullet.strip()}")
    else:
        print("No bullet points found")
    
    # A+ Content
    aplus = listing.get('amazon_aplus_content', '')
    print(f"\nA+ CONTENT ({len(aplus)} chars):")
    if aplus:
        # Show first 1000 chars
        print(aplus[:1000])
        if len(aplus) > 1000:
            print("... [truncated]")
    else:
        print("No A+ content found")
    
    # Keywords
    keywords = listing.get('amazon_keywords', listing.get('keywords', ''))
    print(f"\nFRONTEND KEYWORDS:")
    print(keywords)
    
    # Backend Keywords
    backend_keywords = listing.get('amazon_backend_keywords', '')
    print(f"\nBACKEND KEYWORDS:")
    print(backend_keywords)
    
    return listing

def analyze_australia_quality(listing):
    """Analyze Australia-specific quality"""
    print("\n" + "=" * 80)
    print("AUSTRALIA MARKETPLACE QUALITY ANALYSIS")
    print("=" * 80)
    
    # Get all text content
    title = listing.get('title', '')
    description = listing.get('long_description', listing.get('short_description', ''))
    bullets_raw = listing.get('bullet_points', '')
    aplus = listing.get('amazon_aplus_content', '')
    keywords = listing.get('amazon_keywords', listing.get('keywords', ''))
    backend_keywords = listing.get('amazon_backend_keywords', '')
    
    # Parse bullets
    if bullets_raw:
        if bullets_raw.startswith('[') and bullets_raw.endswith(']'):
            try:
                import ast
                bullets = ast.literal_eval(bullets_raw)
            except:
                bullets = bullets_raw.split('\n') if '\n' in bullets_raw else [bullets_raw]
        else:
            bullets = bullets_raw.split('\n') if '\n' in bullets_raw else [bullets_raw]
    else:
        bullets = []
    
    # Combine all text
    all_text = f"{title} {description}"
    if isinstance(bullets, list):
        all_text += " " + " ".join(bullets)
    all_text += f" {aplus} {backend_keywords}"
    if isinstance(keywords, list):
        all_text += " " + " ".join(keywords)
    
    all_text_lower = all_text.lower()
    
    # Cultural Analysis
    cultural_elements = {
        'australia_day': all_text_lower.count('australia_day') + all_text_lower.count('australia day'),
        'australia': all_text_lower.count('australia'),
        'aussie': all_text_lower.count('aussie'),
        'fair_dinkum': all_text_lower.count('fair dinkum'),
        'mateship': all_text_lower.count('mateship'),
        'mate': all_text_lower.count('mate'),
        'bbq': all_text_lower.count('bbq') + all_text_lower.count('barbecue'),
        'outback': all_text_lower.count('outback'),
        'sydney': all_text_lower.count('sydney'),
        'melbourne': all_text_lower.count('melbourne'),
        'queensland': all_text_lower.count('queensland'),
        'bondi': all_text_lower.count('bondi'),
        'harbour_bridge': all_text_lower.count('harbour bridge'),
        'opera_house': all_text_lower.count('opera house'),
        'extreme_climate': all_text_lower.count('extreme climate'),
        'coastal_living': all_text_lower.count('coastal living')
    }
    
    print("CULTURAL INTEGRATION ANALYSIS:")
    total_cultural = 0
    for element, count in cultural_elements.items():
        if count > 0:
            print(f"  {element.replace('_', ' ').title()}: {count}")
            total_cultural += count
    
    print(f"\nTotal Cultural References: {total_cultural}")
    cultural_score = min(10, total_cultural * 1.5)
    print(f"Cultural Integration Score: {cultural_score}/10")
    
    # A+ Content Analysis
    aplus_score = 0
    if aplus:
        sections = ['hero', 'features', 'comparison', 'lifestyle', 'trust', 'specifications', 'faq', 'guarantee']
        found_sections = [s for s in sections if s in aplus.lower()]
        english_descriptions = aplus.count('ENGLISH:')
        
        print(f"\nA+ CONTENT ANALYSIS:")
        print(f"  Total length: {len(aplus)} characters")
        print(f"  Sections found: {found_sections} ({len(found_sections)}/8)")
        print(f"  ENGLISH descriptions: {english_descriptions}")
        
        # Check for Australian context in A+ content
        aus_contexts = ['australian', 'sydney', 'melbourne', 'queensland', 'bondi', 'harbour bridge', 'uluru', 'great barrier reef']
        aus_context_count = sum(aplus.lower().count(ctx) for ctx in aus_contexts)
        print(f"  Australian context references: {aus_context_count}")
        
        aplus_score = min(10, (len(found_sections) * 1.25) + (english_descriptions * 0.5) + (aus_context_count * 0.5))
    
    print(f"A+ Content Score: {aplus_score}/10")
    
    # Overall Quality Assessment
    content_quality = 0
    if len(title) > 80:
        content_quality += 2
    if len(description) > 800:
        content_quality += 2
    if isinstance(bullets, list) and len(bullets) >= 5:
        content_quality += 2
    if len(aplus) > 10000:
        content_quality += 2
    if 'premium' in all_text_lower or 'professional' in all_text_lower:
        content_quality += 1
    if 'wireless' in all_text_lower and 'gaming' in all_text_lower:
        content_quality += 1
    
    print(f"\nCONTENT QUALITY SCORES:")
    print(f"  Title Quality: {2 if len(title) > 80 else 1 if len(title) > 50 else 0}/2")
    print(f"  Description Quality: {2 if len(description) > 800 else 1 if len(description) > 500 else 0}/2")
    print(f"  Bullet Points: {2 if isinstance(bullets, list) and len(bullets) >= 5 else 0}/2")
    print(f"  A+ Content: {2 if len(aplus) > 10000 else 1 if len(aplus) > 5000 else 0}/2")
    print(f"  Brand Positioning: {1 if 'premium' in all_text_lower or 'professional' in all_text_lower else 0}/1")
    print(f"  Product Relevance: {1 if 'wireless' in all_text_lower and 'gaming' in all_text_lower else 0}/1")
    
    overall_score = (cultural_score + aplus_score + content_quality) / 3
    print(f"\nOVERALL AUSTRALIA QUALITY SCORE: {overall_score:.1f}/10")
    
    if overall_score >= 8:
        grade = "A"
        assessment = "Excellent - Ready for market"
    elif overall_score >= 6:
        grade = "B"
        assessment = "Good - Minor improvements recommended"
    elif overall_score >= 4:
        grade = "C"
        assessment = "Fair - Needs enhancement"
    else:
        grade = "D"
        assessment = "Poor - Significant improvements required"
    
    print(f"Grade: {grade}")
    print(f"Assessment: {assessment}")
    
    # Competitive Analysis Summary
    print(f"\nCOMPETITIVE POSITIONING:")
    print(f"  vs Helium 10: {'Superior' if overall_score >= 8 else 'Competitive' if overall_score >= 6 else 'Needs Improvement'}")
    print(f"  vs Jasper AI: {'Superior' if overall_score >= 7.5 else 'Competitive' if overall_score >= 5.5 else 'Needs Improvement'}")
    print(f"  vs Copy Monkey: {'Superior' if overall_score >= 7 else 'Competitive' if overall_score >= 5 else 'Needs Improvement'}")
    
    return {
        'cultural_score': cultural_score,
        'aplus_score': aplus_score,
        'content_quality': content_quality,
        'overall_score': overall_score,
        'grade': grade,
        'assessment': assessment,
        'cultural_elements': cultural_elements,
        'total_cultural': total_cultural
    }

def save_comprehensive_report(listing, analysis):
    """Save comprehensive HTML report"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en-au">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Australia Marketplace Listing - Comprehensive Analysis</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #e6f3ff 0%, #ffffff 100%);
            color: #333;
            line-height: 1.6;
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
        .flag {{ font-size: 2em; margin-right: 10px; }}
        .score-badge {{
            display: inline-block;
            background: {'#00C851' if analysis['overall_score'] >= 8 else '#33B5E5' if analysis['overall_score'] >= 6 else '#FF8800' if analysis['overall_score'] >= 4 else '#FF4444'};
            color: white;
            padding: 15px 30px;
            border-radius: 30px;
            font-weight: bold;
            font-size: 1.2em;
            margin-top: 15px;
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
            border-bottom: 3px solid #FF6B35;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .content-box {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 15px 0;
            border-left: 4px solid #FF6B35;
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
        .score-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .score-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            text-align: center;
            border-top: 4px solid #FF6B35;
        }}
        .score-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #FF6B35;
            margin: 10px 0;
        }}
        .cultural-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 20px 0;
        }}
        .cultural-tag {{
            background: #FF6B35;
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
        }}
        .competitive-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin: 20px 0;
        }}
        .competitor-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border: 3px solid;
        }}
        .superior {{ border-color: #00C851; background: #f8fff8; }}
        .competitive {{ border-color: #33B5E5; background: #f0f8ff; }}
        .needs-improvement {{ border-color: #FF8800; background: #fff8f0; }}
        .aplus-content {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            max-height: 400px;
            overflow-y: auto;
            font-family: monospace;
            font-size: 0.9em;
            white-space: pre-wrap;
            border: 2px solid #FF6B35;
        }}
        .meta-info {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .meta-card {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #FF6B35;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><span class="flag">🇦🇺</span>Australia Marketplace Analysis</h1>
            <h2>Premium Wireless Gaming Headset Pro by AudioElite</h2>
            <div class="score-badge">
                Overall Score: {analysis['overall_score']:.1f}/10 ({analysis['grade']})
            </div>
            <p style="margin-top: 15px; font-size: 1.1em;">{analysis['assessment']}</p>
        </div>
        
        <div class="section">
            <h2>📋 Product Information</h2>
            <div class="meta-info">
                <div class="meta-card">
                    <strong>Listing ID:</strong> {listing.get('id', 'N/A')}
                </div>
                <div class="meta-card">
                    <strong>Platform:</strong> {listing.get('platform', 'N/A')}
                </div>
                <div class="meta-card">
                    <strong>Status:</strong> {listing.get('status', 'N/A')}
                </div>
                <div class="meta-card">
                    <strong>Created:</strong> {listing.get('created_at', 'N/A')}
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 Quality Score Breakdown</h2>
            <div class="score-grid">
                <div class="score-card">
                    <h4>Cultural Integration</h4>
                    <div class="score-value">{analysis['cultural_score']:.1f}/10</div>
                    <p>{analysis['total_cultural']} cultural references found</p>
                </div>
                <div class="score-card">
                    <h4>A+ Content Quality</h4>
                    <div class="score-value">{analysis['aplus_score']:.1f}/10</div>
                    <p>Professional A+ content</p>
                </div>
                <div class="score-card">
                    <h4>Content Quality</h4>
                    <div class="score-value">{analysis['content_quality']:.1f}/10</div>
                    <p>Overall content excellence</p>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>📝 Product Title</h2>
            <div class="content-box">
                <p style="font-size: 1.2em; font-weight: bold;">
                    {listing.get('title', 'N/A')}
                </p>
                <p><strong>Length:</strong> {len(listing.get('title', ''))} characters</p>
            </div>
        </div>
        
        <div class="section">
            <h2>📖 Product Description</h2>
            <div class="content-box">
                {listing.get('long_description', listing.get('short_description', 'N/A'))}
            </div>
            <p><strong>Length:</strong> {len(listing.get('long_description', listing.get('short_description', '')))} characters</p>
        </div>
        
        <div class="section">
            <h2>🎯 Key Features (Bullet Points)</h2>
            <ul class="bullet-points">
    """
    
    bullets_raw = listing.get('bullet_points', '')
    if bullets_raw:
        if bullets_raw.startswith('[') and bullets_raw.endswith(']'):
            try:
                import ast
                bullets = ast.literal_eval(bullets_raw)
            except:
                bullets = bullets_raw.split('\n') if '\n' in bullets_raw else [bullets_raw]
        else:
            bullets = bullets_raw.split('\n') if '\n' in bullets_raw else [bullets_raw]
        bullets = [b.strip() for b in bullets if b.strip()]  # Remove empty lines
    else:
        bullets = []
    if isinstance(bullets, list) and bullets:
        for bullet in bullets:
            html_content += f"<li>{bullet}</li>"
    else:
        html_content += "<li>No bullet points found</li>"
    
    html_content += f"""
            </ul>
            <p><strong>Count:</strong> {len(bullets) if isinstance(bullets, list) else 0} bullet points</p>
        </div>
        
        <div class="section">
            <h2>🇦🇺 Australian Cultural Integration</h2>
            <p><strong>Total Cultural References: {analysis['total_cultural']}</strong></p>
            <div class="cultural-tags">
    """
    
    for element, count in analysis['cultural_elements'].items():
        if count > 0:
            html_content += f'<span class="cultural-tag">{element.replace("_", " ").title()}: {count}</span>'
    
    html_content += f"""
            </div>
            <p style="margin-top: 20px;">
                <strong>Cultural Integration Score:</strong> {analysis['cultural_score']:.1f}/10
            </p>
        </div>
        
        <div class="section">
            <h2>🎨 A+ Content Preview</h2>
            <div class="aplus-content">
{listing.get('amazon_aplus_content', 'No A+ content found')[:3000]}
            </div>
            <p><strong>Total A+ Content Length:</strong> {len(listing.get('amazon_aplus_content', ''))} characters</p>
        </div>
        
        <div class="section">
            <h2>🥊 Competitive Analysis</h2>
            <div class="competitive-grid">
    """
    
    # Determine competitive status
    score = analysis['overall_score']
    helium_status = 'superior' if score >= 8 else 'competitive' if score >= 6 else 'needs-improvement'
    jasper_status = 'superior' if score >= 7.5 else 'competitive' if score >= 5.5 else 'needs-improvement'
    copy_status = 'superior' if score >= 7 else 'competitive' if score >= 5 else 'needs-improvement'
    
    html_content += f"""
                <div class="competitor-card {helium_status}">
                    <h4>vs Helium 10</h4>
                    <p><strong>{'Superior' if score >= 8 else 'Competitive' if score >= 6 else 'Needs Improvement'}</strong></p>
                </div>
                <div class="competitor-card {jasper_status}">
                    <h4>vs Jasper AI</h4>
                    <p><strong>{'Superior' if score >= 7.5 else 'Competitive' if score >= 5.5 else 'Needs Improvement'}</strong></p>
                </div>
                <div class="competitor-card {copy_status}">
                    <h4>vs Copy Monkey</h4>
                    <p><strong>{'Superior' if score >= 7 else 'Competitive' if score >= 5 else 'Needs Improvement'}</strong></p>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>📈 Final Assessment & Recommendations</h2>
            <div class="content-box">
                <h4>Overall Grade: {analysis['grade']}</h4>
                <h4>Assessment: {analysis['assessment']}</h4>
                <h4>Market Readiness: {'Excellent' if score >= 8 else 'Good' if score >= 6 else 'Needs Enhancement'}</h4>
            </div>
            
            <h4>Key Strengths:</h4>
            <ul>
    """
    
    # Add strengths based on scores
    if analysis['cultural_score'] >= 6:
        html_content += "<li>Strong Australian cultural integration</li>"
    if analysis['aplus_score'] >= 6:
        html_content += "<li>Comprehensive A+ content strategy</li>"
    if analysis['content_quality'] >= 6:
        html_content += "<li>High-quality content structure</li>"
    
    html_content += """
            </ul>
            
            <h4>Improvement Opportunities:</h4>
            <ul>
    """
    
    # Add improvements based on scores
    if analysis['cultural_score'] < 6:
        html_content += "<li>Enhance Australian cultural elements and local references</li>"
    if analysis['aplus_score'] < 6:
        html_content += "<li>Expand A+ content with more sections and Australian imagery</li>"
    if analysis['content_quality'] < 6:
        html_content += "<li>Strengthen content quality and keyword optimization</li>"
    
    html_content += f"""
            </ul>
        </div>
        
        <div class="header" style="background: linear-gradient(135deg, #00C851 0%, #00A652 100%);">
            <h3>🇦🇺 Australia Marketplace Implementation Analysis Complete</h3>
            <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            <p>Listing demonstrates {'excellent' if score >= 8 else 'good' if score >= 6 else 'developing'} Australian marketplace adaptation</p>
        </div>
    </div>
</body>
</html>
    """
    
    filename = f"australia_final_comprehensive_analysis_{timestamp}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\nComprehensive report saved: {filename}")
    return filename

if __name__ == "__main__":
    # Fetch the latest listing (ID 1184 from the previous run)
    listing_id = 1184
    print(f"Fetching listing {listing_id}...")
    
    listing = fetch_listing_detail(listing_id)
    if listing:
        display_listing_content(listing)
        analysis = analyze_australia_quality(listing)
        report_file = save_comprehensive_report(listing, analysis)
        
        print("\n" + "=" * 80)
        print("AUSTRALIA MARKETPLACE EVALUATION COMPLETE!")
        print("=" * 80)
        print(f"Final Score: {analysis['overall_score']:.1f}/10 ({analysis['grade']})")
        print(f"Assessment: {analysis['assessment']}")
        print(f"Report saved: {report_file}")
    else:
        print("Failed to fetch listing content")