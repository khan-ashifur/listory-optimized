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
    
    BRAND_TONES = [
        ('professional', 'Professional'),
        ('casual', 'Casual'),
        ('luxury', 'Luxury'),
        ('playful', 'Playful'),
        ('minimal', 'Minimal'),
        ('bold', 'Bold'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    brand_name = models.CharField(max_length=100)
    brand_tone = models.CharField(max_length=20, choices=BRAND_TONES)
    target_platform = models.CharField(max_length=20, choices=PLATFORMS)
    competitor_urls = models.TextField(help_text="Comma-separated competitor URLs", blank=True, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    categories = models.TextField(help_text="Product categories, comma-separated", blank=True, default="")
    features = models.TextField(help_text="Key features, comma-separated", blank=True, default="")
    target_keywords = models.TextField(help_text="Target keywords, comma-separated", blank=True, default="")
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