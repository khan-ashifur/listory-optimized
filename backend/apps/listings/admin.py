from django.contrib import admin
from .models import GeneratedListing, KeywordResearch, ListingOptimization

@admin.register(GeneratedListing)
class GeneratedListingAdmin(admin.ModelAdmin):
    list_display = ('product', 'platform', 'status', 'created_at')
    list_filter = ('platform', 'status', 'created_at')
    search_fields = ('product__name', 'title')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(KeywordResearch)
class KeywordResearchAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'listing', 'search_volume', 'competition')
    list_filter = ('competition',)
    search_fields = ('keyword',)

@admin.register(ListingOptimization)
class ListingOptimizationAdmin(admin.ModelAdmin):
    list_display = ('listing', 'optimization_type', 'priority', 'implemented')
    list_filter = ('optimization_type', 'priority', 'implemented')
    search_fields = ('suggestion',)