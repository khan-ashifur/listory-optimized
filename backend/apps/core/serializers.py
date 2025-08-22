from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, CompetitorAnalysis


class ProductSerializer(serializers.ModelSerializer):
    """Clean, fresh ProductSerializer designed specifically for Etsy optimization"""
    
    # Override marketplace field to prevent DRF auto-generation issues
    marketplace = serializers.CharField(max_length=15)
    brand_tone = serializers.CharField(max_length=30, required=False, allow_blank=True)
    
    product_urls = serializers.ListField(
        child=serializers.URLField(allow_blank=True),
        required=False,
        write_only=True
    )
    competitor_urls = serializers.ListField(
        child=serializers.URLField(allow_blank=True),
        required=False,
        write_only=True
    )
    competitor_asins = serializers.ListField(
        child=serializers.CharField(max_length=20, allow_blank=True),
        required=False,
        write_only=True
    )

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

    def get_brand_tones_for_platform(self, platform):
        """Return appropriate brand tones based on platform"""
        if platform == 'etsy':
            return Product.ETSY_BRAND_TONES
        else:
            return Product.UNIVERSAL_BRAND_TONES
    
    def get_occasions_for_platform(self, platform):
        """Return appropriate occasions based on platform"""
        if platform == 'etsy':
            return Product.ETSY_OCCASIONS
        else:
            # Return basic occasions for other platforms
            return [
                ('', 'Everyday'),
                ('christmas', 'Christmas'),
                ('valentine_day', "Valentine's Day"),
                ('mothers_day', "Mother's Day"),
                ('fathers_day', "Father's Day"),
                ('birthday', 'Birthday'),
                ('anniversary', 'Anniversary'),
            ]

    def validate_brand_tone(self, value):
        """Smart validation for brand_tone based on target_platform"""
        if not value:  # Allow empty brand_tone
            return value
            
        # Get target_platform from initial_data
        target_platform = self.initial_data.get('target_platform', '')
        
        # Get valid choices for this platform
        if target_platform == 'etsy':
            valid_choices = [choice[0] for choice in Product.ETSY_BRAND_TONES]
        else:
            valid_choices = [choice[0] for choice in Product.UNIVERSAL_BRAND_TONES]
        
        # Add empty choice as valid
        valid_choices.append('')
        
        if value not in valid_choices:
            raise serializers.ValidationError(
                f"'{value}' is not a valid brand tone for {target_platform}. "
                f"Valid options: {valid_choices}"
            )
        
        return value

    def validate_marketplace(self, value):
        """Validate marketplace choice"""
        valid_marketplaces = [choice[0] for choice in Product.ALL_MARKETPLACES]
        if value not in valid_marketplaces:
            raise serializers.ValidationError(
                f"'{value}' is not a valid marketplace. Valid options: {valid_marketplaces}"
            )
        return value

    def create(self, validated_data):
        """Clean creation without console output issues"""
        # Handle list fields
        product_urls_list = validated_data.pop('product_urls', [])
        competitor_urls_list = validated_data.pop('competitor_urls', [])
        competitor_asins_list = validated_data.pop('competitor_asins', [])
        
        # Convert lists to comma-separated strings for storage
        if product_urls_list:
            validated_data['product_urls'] = ','.join(filter(None, product_urls_list))
        if competitor_urls_list:
            validated_data['competitor_urls'] = ','.join(filter(None, competitor_urls_list))
        if competitor_asins_list:
            validated_data['competitor_asins'] = ','.join(filter(None, competitor_asins_list))
        
        # Create or get demo user
        user, created = User.objects.get_or_create(
            username='demo_user',
            defaults={'email': 'demo@listory.ai', 'first_name': 'Demo', 'last_name': 'User'}
        )
        validated_data['user'] = user
        
        # Auto-detect brand_tone if empty for Etsy
        if not validated_data.get('brand_tone') and validated_data.get('target_platform') == 'etsy':
            validated_data['brand_tone'] = self.auto_detect_etsy_brand_tone(validated_data)
        
        # Auto-set marketplace to 'etsy' if target_platform is 'etsy'
        if validated_data.get('target_platform') == 'etsy' and not validated_data.get('marketplace'):
            validated_data['marketplace'] = 'etsy'
        
        return super().create(validated_data)

    def auto_detect_etsy_brand_tone(self, data):
        """AI-powered brand tone detection for Etsy products"""
        name = data.get('name', '').lower()
        description = data.get('description', '').lower()
        features = data.get('features', '').lower()
        
        combined_text = f"{name} {description} {features}"
        
        # Keywords mapping for automatic detection
        tone_keywords = {
            'handmade_artisan': ['handmade', 'artisan', 'crafted', 'handcrafted', 'made by hand'],
            'vintage_charm': ['vintage', 'retro', 'antique', 'classic', 'timeless', 'nostalgic'],
            'bohemian_free': ['bohemian', 'boho', 'free spirit', 'wanderlust', 'hippie', 'eclectic'],
            'cottagecore_cozy': ['cottage', 'cozy', 'farmhouse', 'rustic', 'country', 'pastoral'],
            'modern_minimalist': ['minimal', 'clean', 'simple', 'geometric', 'sleek', 'contemporary'],
            'whimsical_playful': ['whimsical', 'playful', 'fun', 'quirky', 'cute', 'magical'],
            'eco_conscious': ['eco', 'sustainable', 'organic', 'natural', 'bamboo', 'recycled'],
            'luxury_handcrafted': ['luxury', 'premium', 'high-end', 'elegant', 'sophisticated'],
            'artistic_creative': ['artistic', 'creative', 'unique', 'original', 'expressive'],
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


class CompetitorAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitorAnalysis
        fields = '__all__'