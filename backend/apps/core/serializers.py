from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, CompetitorAnalysis


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

    def create(self, validated_data):
        # For demo, create or get a default user
        try:
            user, created = User.objects.get_or_create(
                username='demo_user',
                defaults={'email': 'demo@listory.ai', 'first_name': 'Demo', 'last_name': 'User'}
            )
            validated_data['user'] = user
            print(f"Creating product with data: {validated_data}")  # Debug log
            return super().create(validated_data)
        except Exception as e:
            print(f"Error creating product: {e}")  # Debug log
            raise e


class CompetitorAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitorAnalysis
        fields = '__all__'