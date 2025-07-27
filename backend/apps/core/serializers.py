from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, CompetitorAnalysis


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

    def create(self, validated_data):
        import sys
        import io
        
        # Redirect stdout/stderr to prevent console Unicode issues during model creation
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        
        try:
            sys.stdout = io.StringIO()
            sys.stderr = io.StringIO()
            
            # For demo, create or get a default user
            user, created = User.objects.get_or_create(
                username='demo_user',
                defaults={'email': 'demo@listory.ai', 'first_name': 'Demo', 'last_name': 'User'}
            )
            validated_data['user'] = user
            
            # Create the product with output redirected
            product = super().create(validated_data)
            return product
            
        finally:
            # Always restore stdout/stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr


class CompetitorAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitorAnalysis
        fields = '__all__'