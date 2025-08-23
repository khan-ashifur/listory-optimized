from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    PLATFORMS = [
        ('amazon', 'Amazon'),
        ('walmart', 'Walmart'),
        ('etsy', 'Etsy'),
        ('tiktok', 'TikTok'),
        ('shopify', 'Shopify'),
    ]
    
    # Universal brand tones for Amazon/Walmart
    UNIVERSAL_BRAND_TONES = [
        ('professional', 'Professional'),
        ('casual', 'Casual'),
        ('luxury', 'Luxury'),
        ('trendy', 'Trendy'),
        ('playful', 'Playful'),
        ('minimal', 'Minimal'),
        ('bold', 'Bold'),
    ]
    
    # Mexican-specific brand tones based on cultural research
    MEXICAN_BRAND_TONES = [
        ('familiar_caloroso', 'Familiar y Cálido'),          # Warm and family-oriented
        ('tradicion_mexicana', 'Tradición Mexicana'),        # Mexican tradition
        ('lujo_mexicano', 'Lujo Mexicano'),                  # Mexican luxury  
        ('joven_vibrante', 'Joven y Vibrante'),              # Young and vibrant
        ('confiable_profesional', 'Confiable y Profesional'), # Trustworthy professional
        ('festivo_celebracion', 'Festivo y Celebración'),    # Festive and celebratory
        ('moderno_mexicano', 'Moderno Mexicano'),            # Modern Mexican
        ('hogareño_familiar', 'Hogareño y Familiar'),        # Home and family focused
    ]
    
    # Etsy-specific brand tones based on 2025 research  
    ETSY_BRAND_TONES = [
        ('handmade_artisan', 'Handmade Artisan'),
        ('vintage_charm', 'Vintage Charm'),
        ('bohemian_free', 'Bohemian Free-Spirit'),
        ('cottagecore_cozy', 'Cottagecore Cozy'),
        ('modern_minimalist', 'Modern Minimalist'),
        ('whimsical_playful', 'Whimsical & Playful'),
        ('rustic_farmhouse', 'Rustic Farmhouse'),
        ('eco_conscious', 'Eco-Conscious'),
        ('luxury_handcrafted', 'Luxury Handcrafted'),
        ('artistic_creative', 'Artistic & Creative'),
        ('messy_coquette', 'Messy Coquette'),  # 2025 trend
        ('chateaucore', 'Châteaucore'),        # 2025 trend
        ('galactic_metallic', 'Galactic Metallic'), # 2025 trend
    ]
    
    # Combined brand tones - dynamically created based on platform
    BRAND_TONES = [('', 'Select')] + UNIVERSAL_BRAND_TONES + MEXICAN_BRAND_TONES + ETSY_BRAND_TONES
    
    AMAZON_MARKETPLACES = [
        ('us', 'United States'),
        ('ca', 'Canada'),
        ('mx', 'Mexico'),
        ('uk', 'United Kingdom'),
        ('de', 'Germany'),
        ('fr', 'France'),
        ('it', 'Italy'),
        ('es', 'Spain'),
        ('nl', 'Netherlands'),
        ('se', 'Sweden'),
        ('pl', 'Poland'),
        ('be', 'Belgium'),
        ('jp', 'Japan'),
        ('in', 'India'),
        ('sg', 'Singapore'),
        ('ae', 'UAE'),
        ('sa', 'Saudi Arabia'),
        ('br', 'Brazil'),
        ('au', 'Australia'),
        ('tr', 'Turkey'),
        ('eg', 'Egypt'),
    ]
    
    WALMART_MARKETPLACES = [
        ('walmart_usa', 'Walmart USA'),
        ('walmart_canada', 'Walmart Canada'),
        ('walmart_mexico', 'Walmart Mexico'),
    ]
    
    ETSY_MARKETPLACES = [
        ('etsy', 'Etsy'),
    ]
    
    ALL_MARKETPLACES = AMAZON_MARKETPLACES + WALMART_MARKETPLACES + ETSY_MARKETPLACES
    
    # Mexican-specific occasions based on cultural traditions  
    MEXICAN_OCCASIONS = [
        ('', 'Uso Diario/Sin Ocasión Específica'),
        # Major Mexican holidays
        ('navidad', 'Navidad'),                    # Christmas
        ('dia_reyes', 'Día de Reyes'),             # Three Kings Day
        ('dia_madre', 'Día de las Madres'),        # Mother's Day (May 10)
        ('dia_padre', 'Día del Padre'),            # Father's Day  
        ('dia_muertos', 'Día de los Muertos'),     # Day of the Dead
        ('independence_day', 'Día de la Independencia'), # Sept 16
        ('guadalupe', 'Día de la Virgen de Guadalupe'),  # Dec 12
        # Life celebrations
        ('quinceañera', 'Quinceañera'),            # 15th birthday
        ('boda', 'Boda'),                          # Wedding
        ('bautizo', 'Bautizo'),                    # Baptism
        ('primera_comunion', 'Primera Comunión'),  # First Communion
        ('graduacion', 'Graduación'),              # Graduation
        ('cumpleaños', 'Cumpleaños'),              # Birthday
        # Shopping seasons
        ('regreso_clases', 'Regreso a Clases'),    # Back to school
        ('hot_sale', 'Hot Sale'),                  # Major shopping event
        ('buen_fin', 'El Buen Fin'),               # Mexican Black Friday
        # Cultural events
        ('grito', 'El Grito'),                     # Independence celebration
        ('posadas', 'Las Posadas'),                # Christmas celebration period
        ('año_nuevo', 'Año Nuevo'),                # New Year
    ]
    
    # Etsy-specific occasions based on 2025 trends and research
    ETSY_OCCASIONS = [
        ('', 'Everyday/No Specific Occasion'),
        # Major holidays
        ('christmas_2025', 'Christmas 2025'),
        ('valentine_day', "Valentine's Day"),
        ('mothers_day', "Mother's Day"),
        ('fathers_day', "Father's Day"),
        ('easter', 'Easter'),
        ('halloween', 'Halloween'),
        ('thanksgiving', 'Thanksgiving'),
        ('new_year', 'New Year'),
        # Life events
        ('wedding', 'Wedding'),
        ('anniversary', 'Anniversary'),
        ('birthday', 'Birthday'),
        ('baby_shower', 'Baby Shower'),
        ('graduation', 'Graduation'),
        ('housewarming', 'Housewarming'),
        # Seasonal trends based on research
        ('spring_refresh', 'Spring Home Refresh'),
        ('summer_vibes', 'Summer Vibes'),
        ('fall_cozy', 'Fall Cozy Season'),
        ('winter_comfort', 'Winter Comfort'),
        # 2025 specific trends
        ('galactic_theme', 'Galactic/Space Theme'),
        ('cottagecore_trend', 'Cottagecore Aesthetic'),
        ('vintage_revival', 'Vintage Revival'),
        ('sustainability', 'Eco-Friendly/Sustainable'),
        ('self_care', 'Self-Care & Wellness'),
        ('work_from_home', 'Work From Home Setup'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    brand_name = models.CharField(max_length=100)
    brand_tone = models.CharField(max_length=30, choices=BRAND_TONES, blank=True, default="")
    target_platform = models.CharField(max_length=20, choices=PLATFORMS)
    
    # Platform-specific fields
    asin = models.CharField(max_length=20, blank=True, default="", help_text="Amazon Standard Identification Number")
    marketplace = models.CharField(max_length=15, choices=ALL_MARKETPLACES, default='us', help_text="Marketplace/country for the platform")
    marketplace_language = models.CharField(max_length=10, blank=True, default="en", help_text="Language for the selected marketplace")
    brand_persona = models.TextField(blank=True, default="", help_text="Brand personality, values, and voice")
    target_audience = models.TextField(blank=True, default="", help_text="Description of ideal customer demographics and psychographics")
    competitor_asins = models.TextField(help_text="Comma-separated competitor ASINs", blank=True, default="")
    product_urls = models.TextField(help_text="Product reference URLs, comma-separated (max 3)", blank=True, default="")
    
    competitor_urls = models.TextField(help_text="Comma-separated competitor URLs", blank=True, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    categories = models.TextField(help_text="Product categories, comma-separated", blank=True, default="")
    features = models.TextField(help_text="Key features, comma-separated", blank=True, default="")
    target_keywords = models.TextField(help_text="Target keywords, comma-separated", blank=True, default="")
    occasion = models.CharField(max_length=100, help_text="Special occasion for targeted content (e.g., Christmas, Valentine's Day)", blank=True, default="")
    seo_keywords = models.TextField(help_text="Primary SEO keywords for search optimization", blank=True, default="")
    long_tail_keywords = models.TextField(help_text="Long-tail keywords for specific searches", blank=True, default="")
    faqs = models.TextField(help_text="Frequently asked questions and answers", blank=True, default="")
    whats_in_box = models.TextField(help_text="List of items included in the package", blank=True, default="")
    
    # Product image
    product_image = models.ImageField(upload_to='products/', null=True, blank=True, help_text="Upload your product image")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.target_platform}"

    class Meta:
        ordering = ['-created_at']


class CompetitorAnalysis(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    url = models.URLField()
    title = models.CharField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    review_count = models.IntegerField(null=True, blank=True)
    key_features = models.TextField(blank=True)
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis for {self.product.name} - {self.url}"