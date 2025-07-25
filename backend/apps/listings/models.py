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
    amazon_backend_keywords = models.TextField(blank=True)
    
    tiktok_video_script = models.TextField(blank=True)
    tiktok_hashtags = models.TextField(blank=True)
    tiktok_hooks = models.TextField(blank=True)
    
    etsy_tags = models.TextField(blank=True)
    etsy_materials = models.TextField(blank=True)
    
    walmart_key_features = models.TextField(blank=True)
    walmart_specifications = models.TextField(blank=True)
    
    shopify_seo_title = models.TextField(blank=True)
    shopify_meta_description = models.TextField(blank=True)
    
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