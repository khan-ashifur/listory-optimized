from django.db import models
from apps.core.models import Product


class GeneratedListing(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    platform = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Common fields for all platforms
    title = models.CharField(max_length=500, blank=True)
    short_description = models.TextField(blank=True)
    long_description = models.TextField(blank=True)
    bullet_points = models.TextField(blank=True)
    keywords = models.TextField(blank=True)
    
    # Platform-specific fields
    amazon_aplus_content = models.TextField(blank=True, help_text="Amazon A+ content suggestions")
    amazon_keywords = models.TextField(blank=True, help_text="Amazon frontend display keywords")
    amazon_backend_keywords = models.TextField(blank=True)
    
    # A+ Content fields
    hero_title = models.TextField(blank=True)
    hero_content = models.TextField(blank=True)
    features = models.TextField(blank=True)
    whats_in_box = models.TextField(blank=True)
    trust_builders = models.TextField(blank=True)
    faqs = models.TextField(blank=True)
    social_proof = models.TextField(blank=True)
    guarantee = models.TextField(blank=True)
    
    tiktok_video_script = models.TextField(blank=True)
    tiktok_hashtags = models.TextField(blank=True)
    tiktok_hooks = models.TextField(blank=True)
    
    # Etsy-specific fields (comprehensive implementation)
    etsy_title = models.CharField(max_length=140, blank=True, help_text="Etsy title (max 140 characters)")
    etsy_tags = models.TextField(blank=True, help_text="13 Etsy tags (JSON array, max 20 chars each)")
    etsy_description = models.TextField(blank=True, help_text="Etsy description (max 102,400 chars)")
    etsy_materials = models.TextField(blank=True, help_text="Materials used in creation")
    etsy_processing_time = models.CharField(max_length=50, blank=True, help_text="Processing time for orders")
    etsy_personalization = models.TextField(blank=True, help_text="Personalization options available")
    
    # Etsy who made choices
    ETSY_WHO_MADE_CHOICES = [
        ('i_did', 'I did'),
        ('collective', 'A member of my shop'),
        ('someone_else', 'Another company or person'),
    ]
    etsy_who_made = models.CharField(max_length=20, choices=ETSY_WHO_MADE_CHOICES, blank=True, help_text="Who made this item")
    
    # Etsy when made choices
    ETSY_WHEN_MADE_CHOICES = [
        ('made_to_order', 'Made to order'),
        ('2020_2024', '2020-2024'),
        ('2010_2019', '2010-2019'),
        ('2000_2009', '2000-2009'),
        ('1990s', '1990s'),
        ('1980s', '1980s'),
        ('1970s', '1970s'),
        ('1960s', '1960s'),
        ('1950s', '1950s'),
        ('1940s', '1940s'),
        ('1930s', '1930s'),
        ('1920s', '1920s'),
        ('1910s', '1910s'),
        ('1900s', '1900s'),
        ('1800s', '1800s'),
        ('before_1800', 'Before 1800'),
    ]
    etsy_when_made = models.CharField(max_length=20, choices=ETSY_WHEN_MADE_CHOICES, blank=True, help_text="When was this item made")
    
    etsy_category_path = models.CharField(max_length=500, blank=True, help_text="Etsy category hierarchy")
    etsy_attributes = models.TextField(blank=True, help_text="Etsy-specific attributes (JSON)")
    etsy_section_id = models.CharField(max_length=50, blank=True, help_text="Shop section ID")
    etsy_production_partners = models.TextField(blank=True, help_text="Production partner information")
    etsy_shipping_profile = models.TextField(blank=True, help_text="Shipping profile information (JSON)")
    
    # Additional Etsy optimization fields
    etsy_style_tags = models.TextField(blank=True, help_text="Style-specific tags for better discovery")
    etsy_seasonal_keywords = models.TextField(blank=True, help_text="Seasonal keywords for occasions")
    etsy_target_demographics = models.TextField(blank=True, help_text="Target buyer demographics")
    etsy_gift_suggestions = models.TextField(blank=True, help_text="Gift occasion suggestions")
    etsy_care_instructions = models.TextField(blank=True, help_text="Care and maintenance instructions")
    etsy_size_guide = models.TextField(blank=True, help_text="Size guide information")
    etsy_story_behind = models.TextField(blank=True, help_text="Story behind the creation")
    etsy_sustainability_info = models.TextField(blank=True, help_text="Sustainability and eco-friendly information")
    etsy_visual_suggestions = models.TextField(blank=True, help_text="Photo styling suggestions and visual recommendations")
    etsy_value_proposition = models.TextField(blank=True, help_text="Quality justification and value positioning")
    
    # 🎉 WOW FEATURES - REVOLUTIONARY ADDITIONS NO ONE ELSE OFFERS!
    etsy_shop_setup_guide = models.TextField(blank=True, help_text="Complete Etsy shop setup guide with branding, policies, goals")
    etsy_social_media_package = models.TextField(blank=True, help_text="30-day social media content calendar and templates")
    etsy_seasonal_calendar = models.TextField(blank=True, help_text="12-month marketing and promotional calendar")
    etsy_photography_guide = models.TextField(blank=True, help_text="Professional photography styling guide with lighting and props")
    etsy_customer_service_templates = models.TextField(blank=True, help_text="Professional email templates for customer communication")
    etsy_pricing_analysis = models.TextField(blank=True, help_text="Comprehensive pricing strategy and competitive analysis")
    etsy_competitor_insights = models.TextField(blank=True, help_text="Market research and competitor analysis insights")
    etsy_policies_templates = models.TextField(blank=True, help_text="Complete shop policies templates (returns, shipping, privacy)")
    etsy_variations_guide = models.TextField(blank=True, help_text="Product variations and upselling opportunities guide")
    etsy_seo_report = models.TextField(blank=True, help_text="Advanced SEO optimization report and ranking strategies")
    
    # Walmart-specific fields (marketplace requirements)
    walmart_product_title = models.CharField(max_length=100, blank=True, help_text="Walmart product title (100 char hard limit)")
    walmart_description = models.TextField(blank=True, help_text="Plain text narrative description (min 150 words)")
    walmart_key_features = models.TextField(blank=True, help_text="3-10 bullet points, max 80 chars each, plain text only")
    walmart_specifications = models.TextField(blank=True, help_text="Technical specifications JSON")
    
    # Walmart identifiers
    walmart_gtin_upc = models.CharField(max_length=14, blank=True, help_text="GTIN/UPC code")
    walmart_manufacturer_part = models.CharField(max_length=100, blank=True, help_text="Manufacturer part number")
    walmart_sku_id = models.CharField(max_length=50, blank=True, help_text="SKU identifier")
    
    # Walmart attributes
    walmart_product_type = models.CharField(max_length=100, blank=True, help_text="Product type/category")
    walmart_category_path = models.CharField(max_length=500, blank=True, help_text="Category hierarchy")
    walmart_attributes = models.TextField(blank=True, help_text="Category-specific attributes JSON")
    
    # Walmart shipping info
    walmart_shipping_weight = models.CharField(max_length=50, blank=True, help_text="Shipping weight with unit")
    walmart_shipping_dimensions = models.TextField(blank=True, help_text="L x W x H dimensions")
    
    # Walmart compliance
    walmart_warranty_info = models.TextField(blank=True, help_text="Warranty details")
    walmart_compliance_certifications = models.TextField(blank=True, help_text="Safety/compliance certs")
    walmart_assembly_required = models.BooleanField(default=False, help_text="Assembly required flag")
    
    # Walmart rich media
    walmart_video_urls = models.TextField(blank=True, help_text="Product video URLs")
    walmart_swatch_images = models.TextField(blank=True, help_text="Swatch/variant images")
    
    shopify_seo_title = models.TextField(blank=True)
    shopify_meta_description = models.TextField(blank=True)
    
    # Quality validation scores
    quality_score = models.FloatField(null=True, blank=True, help_text="Overall quality score (0-10)")
    emotion_score = models.FloatField(null=True, blank=True, help_text="Emotional engagement score (0-10)")
    conversion_score = models.FloatField(null=True, blank=True, help_text="Conversion optimization score (0-10)")
    trust_score = models.FloatField(null=True, blank=True, help_text="Trust and credibility score (0-10)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.platform} Listing"

    class Meta:
        ordering = ['-created_at']


class KeywordResearch(models.Model):
    listing = models.ForeignKey(GeneratedListing, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=200)
    search_volume = models.IntegerField(null=True, blank=True)
    competition = models.CharField(max_length=20, blank=True)
    relevance_score = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.keyword} - {self.listing.product.name}"


class ListingOptimization(models.Model):
    listing = models.ForeignKey(GeneratedListing, on_delete=models.CASCADE)
    optimization_type = models.CharField(max_length=50)
    suggestion = models.TextField()
    priority = models.CharField(max_length=20, choices=[
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low')
    ])
    implemented = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.optimization_type} for {self.listing.product.name}"


class ListingImage(models.Model):
    IMAGE_TYPE_CHOICES = [
        ('hero', 'Hero Shot'),
        ('infographic', 'Infographic'),
        ('lifestyle', 'Lifestyle'),
        ('testimonial', 'Testimonial'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('generating', 'Generating'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    listing = models.ForeignKey(GeneratedListing, on_delete=models.CASCADE, related_name='images')
    image_type = models.CharField(max_length=20, choices=IMAGE_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    prompt = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['listing', 'image_type']
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.get_image_type_display()} for {self.listing.product.name}"