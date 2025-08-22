import os
import sys
import django

# Setup Django
backend_path = os.path.join(os.getcwd(), 'backend')
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product

# Check the latest created product
latest_product = Product.objects.filter(target_platform='etsy').last()
if latest_product:
    print(f"Latest Etsy product:")
    print(f"  ID: {latest_product.id}")
    print(f"  Name: {latest_product.name}")
    print(f"  Brand Tone: '{latest_product.brand_tone}'")
    print(f"  Marketplace: '{latest_product.marketplace}'")
    print(f"  Target Platform: '{latest_product.target_platform}'")
else:
    print("No Etsy products found")

# Test the auto-detection logic directly
data = {
    'name': 'Handmade Ceramic Coffee Mug',
    'description': 'Beautiful handcrafted ceramic mug made by hand with artistic flair',
    'features': 'Handcrafted ceramic\nArtisan made\nUnique patterns',
}

def auto_detect_etsy_brand_tone(data):
    """Test the auto-detection logic"""
    name = data.get('name', '').lower()
    description = data.get('description', '').lower()
    features = data.get('features', '').lower()
    
    combined_text = f"{name} {description} {features}"
    print(f"\nCombined text for detection: '{combined_text}'")
    
    # Keywords mapping for automatic detection based on 2025 Etsy research
    tone_keywords = {
        'handmade_artisan': ['handmade', 'artisan', 'crafted', 'handcrafted', 'made by hand', 'craft'],
        'vintage_charm': ['vintage', 'retro', 'antique', 'classic', 'timeless', 'nostalgic'],
        'bohemian_free': ['bohemian', 'boho', 'free spirit', 'wanderlust', 'hippie', 'eclectic'],
        'cottagecore_cozy': ['cottage', 'cozy', 'farmhouse', 'rustic', 'country', 'pastoral'],
        'modern_minimalist': ['minimal', 'clean', 'simple', 'geometric', 'sleek', 'contemporary'],
        'whimsical_playful': ['whimsical', 'playful', 'fun', 'quirky', 'cute', 'magical'],
        'eco_conscious': ['eco', 'sustainable', 'organic', 'natural', 'bamboo', 'recycled'],
        'luxury_handcrafted': ['luxury', 'premium', 'high-end', 'elegant', 'sophisticated'],
        'artistic_creative': ['artistic', 'creative', 'unique', 'original', 'expressive', 'art'],
        'messy_coquette': ['coquette', 'feminine', 'ruffles', 'bows', 'pink', 'girly'],
        'chateaucore': ['french', 'chateau', 'romantic', 'ornate', 'baroque', 'elegant'],
        'galactic_metallic': ['metallic', 'chrome', 'silver', 'holographic', 'futuristic', 'space'],
    }
    
    # Score each tone based on keyword matches
    tone_scores = {}
    for tone, keywords in tone_keywords.items():
        score = sum(1 for keyword in keywords if keyword in combined_text)
        if score > 0:
            tone_scores[tone] = score
            print(f"  {tone}: {score} matches")
    
    # Return the tone with highest score, or default
    if tone_scores:
        best_tone = max(tone_scores, key=tone_scores.get)
        print(f"\nBest tone: {best_tone}")
        return best_tone
    
    # Default to handmade_artisan for Etsy
    print("\nNo matches found, defaulting to handmade_artisan")
    return 'handmade_artisan'

result = auto_detect_etsy_brand_tone(data)
print(f"\nDetected tone: {result}")