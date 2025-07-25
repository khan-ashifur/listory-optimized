from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet
from .test_views import test_api

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('test/', test_api, name='test_api'),
]