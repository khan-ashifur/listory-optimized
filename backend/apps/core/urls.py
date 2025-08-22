from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, create_product_simple
from .test_views import test_api
from .views_etsy import create_etsy_product, get_etsy_brand_tones, get_etsy_occasions

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('test/', test_api, name='test_api'),
    path('create-product/', create_product_simple, name='create_product_simple'),
    # Etsy-specific endpoints (must come before router.urls)
    path('etsy/create/', create_etsy_product, name='create_etsy_product'),
    path('etsy/brand-tones/', get_etsy_brand_tones, name='etsy_brand_tones'),
    path('etsy/occasions/', get_etsy_occasions, name='etsy_occasions'),
] + router.urls