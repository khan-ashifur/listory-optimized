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


class QualityValidationInputSerializer(serializers.Serializer):
    """Serializer for quality validation input data."""
    title = serializers.CharField(max_length=500, required=True)
    bullet_points = serializers.CharField(required=False, allow_blank=True)
    long_description = serializers.CharField(required=False, allow_blank=True)
    faqs = serializers.CharField(required=False, allow_blank=True)


class QualityValidationOutputSerializer(serializers.Serializer):
    """Serializer for quality validation output data."""
    overall_score = serializers.FloatField()
    max_score = serializers.FloatField()
    grade = serializers.CharField()
    emotion_score = serializers.FloatField()
    conversion_score = serializers.FloatField()
    trust_score = serializers.FloatField()
    summary = serializers.CharField()
    section_scores = serializers.ListField()
    issues = serializers.ListField()
    action_items = serializers.ListField()