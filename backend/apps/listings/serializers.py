from rest_framework import serializers
from .models import GeneratedListing, KeywordResearch, ListingOptimization, ListingImage


class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = '__all__'


class GeneratedListingSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    images = ListingImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = GeneratedListing
        fields = '__all__'


class KeywordResearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeywordResearch
        fields = '__all__'


class ListingOptimizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingOptimization
        fields = '__all__'