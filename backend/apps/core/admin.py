from django.contrib import admin
from .models import Product, CompetitorAnalysis

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand_name', 'target_platform', 'user', 'created_at')
    list_filter = ('target_platform', 'brand_tone', 'created_at')
    search_fields = ('name', 'brand_name', 'description')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(CompetitorAnalysis)
class CompetitorAnalysisAdmin(admin.ModelAdmin):
    list_display = ('product', 'url', 'price', 'rating', 'analyzed_at')
    list_filter = ('analyzed_at',)
    readonly_fields = ('analyzed_at',)