from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, create_product_simple
from .test_views import test_api

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('test/', test_api, name='test_api'),
    path('create-product/', create_product_simple, name='create_product_simple'),
    path('', include(router.urls)),
]