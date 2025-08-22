from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Product
import json


@api_view(['POST'])
@permission_classes([AllowAny])
def create_etsy_product(request):
    """
    Clean Etsy product creation endpoint that bypasses DRF validation issues
    """
    try:
        data = request.data
        
        # Create or get demo user
        user, created = User.objects.get_or_create(
            username='demo_user',
            defaults={'email': 'demo@listory.ai', 'first_name': 'Demo', 'last_name': 'User'}
        )
        
        # Auto-detect brand_tone if not provided
        brand_tone = data.get('brand_tone', '')
        if not brand_tone and data.get('target_platform') == 'etsy':
            brand_tone = auto_detect_etsy_brand_tone(data)
        
        # Create product with Etsy defaults
        product = Product.objects.create(
            user=user,
            name=data.get('name', ''),
            description=data.get('description', ''),
            brand_name=data.get('brand_name', ''),
            brand_tone=brand_tone,
            target_platform='etsy',
            marketplace='etsy',
            marketplace_language='en',
            price=data.get('price'),
            categories=data.get('categories', ''),
            features=data.get('features', ''),
            target_keywords=data.get('target_keywords', ''),
            occasion=data.get('occasion', ''),
            seo_keywords=data.get('seo_keywords', ''),
            long_tail_keywords=data.get('long_tail_keywords', ''),
            faqs=data.get('faqs', ''),
            whats_in_box=data.get('whats_in_box', ''),
            competitor_urls=data.get('competitor_urls', ''),
            product_urls=data.get('product_urls', ''),
            competitor_asins=data.get('competitor_asins', ''),
            brand_persona=data.get('brand_persona', ''),
            target_audience=data.get('target_audience', ''),
        )
        
        # Return comprehensive response
        return Response({
            'id': product.id,
            'name': product.name,
            'brand_name': product.brand_name,
            'brand_tone': product.brand_tone,
            'target_platform': product.target_platform,
            'marketplace': product.marketplace,
            'created_at': product.created_at.isoformat(),
            'status': 'created',
            'message': 'Etsy product created successfully with auto-detected brand tone'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'error': str(e),
            'message': 'Etsy product creation failed'
        }, status=status.HTTP_400_BAD_REQUEST)


def auto_detect_etsy_brand_tone(data):
    """AI-powered brand tone detection for Etsy products"""
    name = data.get('name', '').lower()
    description = data.get('description', '').lower()
    features = data.get('features', '').lower()
    
    combined_text = f"{name} {description} {features}"
    
    # Keywords mapping for automatic detection
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
    
    # Return the tone with highest score, or default
    if tone_scores:
        best_tone = max(tone_scores, key=tone_scores.get)
        return best_tone
    
    # Default to handmade_artisan for Etsy
    return 'handmade_artisan'


@api_view(['GET'])
@permission_classes([AllowAny])
def get_etsy_brand_tones(request):
    """Get Etsy-specific brand tones"""
    return Response({
        'brand_tones': [
            {'value': '', 'label': 'Auto-Detect (Recommended)'},
            {'value': 'handmade_artisan', 'label': 'Handmade Artisan'},
            {'value': 'vintage_charm', 'label': 'Vintage Charm'},
            {'value': 'bohemian_free', 'label': 'Bohemian Free-Spirit'},
            {'value': 'cottagecore_cozy', 'label': 'Cottagecore Cozy'},
            {'value': 'modern_minimalist', 'label': 'Modern Minimalist'},
            {'value': 'whimsical_playful', 'label': 'Whimsical & Playful'},
            {'value': 'rustic_farmhouse', 'label': 'Rustic Farmhouse'},
            {'value': 'eco_conscious', 'label': 'Eco-Conscious'},
            {'value': 'luxury_handcrafted', 'label': 'Luxury Handcrafted'},
            {'value': 'artistic_creative', 'label': 'Artistic & Creative'},
            {'value': 'messy_coquette', 'label': 'Messy Coquette (2025 Trend)'},
            {'value': 'chateaucore', 'label': 'Châteaucore (2025 Trend)'},
            {'value': 'galactic_metallic', 'label': 'Galactic Metallic (2025 Trend)'},
        ]
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_etsy_occasions(request):
    """Get Etsy-specific occasions"""
    return Response({
        'occasions': [
            {'value': '', 'label': 'Everyday/No Specific Occasion'},
            # Major holidays
            {'value': 'christmas_2025', 'label': 'Christmas 2025'},
            {'value': 'valentine_day', 'label': "Valentine's Day"},
            {'value': 'mothers_day', 'label': "Mother's Day"},
            {'value': 'fathers_day', 'label': "Father's Day"},
            {'value': 'easter', 'label': 'Easter'},
            {'value': 'halloween', 'label': 'Halloween'},
            {'value': 'thanksgiving', 'label': 'Thanksgiving'},
            {'value': 'new_year', 'label': 'New Year'},
            # Life events
            {'value': 'wedding', 'label': 'Wedding'},
            {'value': 'anniversary', 'label': 'Anniversary'},
            {'value': 'birthday', 'label': 'Birthday'},
            {'value': 'baby_shower', 'label': 'Baby Shower'},
            {'value': 'graduation', 'label': 'Graduation'},
            {'value': 'housewarming', 'label': 'Housewarming'},
            # Seasonal trends
            {'value': 'spring_refresh', 'label': 'Spring Home Refresh'},
            {'value': 'summer_vibes', 'label': 'Summer Vibes'},
            {'value': 'fall_cozy', 'label': 'Fall Cozy Season'},
            {'value': 'winter_comfort', 'label': 'Winter Comfort'},
            # 2025 trends
            {'value': 'galactic_theme', 'label': 'Galactic/Space Theme'},
            {'value': 'cottagecore_trend', 'label': 'Cottagecore Aesthetic'},
            {'value': 'vintage_revival', 'label': 'Vintage Revival'},
            {'value': 'sustainability', 'label': 'Eco-Friendly/Sustainable'},
            {'value': 'self_care', 'label': 'Self-Care & Wellness'},
            {'value': 'work_from_home', 'label': 'Work From Home Setup'},
        ]
    })