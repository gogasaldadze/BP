from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

urlpatterns = []


router = DefaultRouter()
router.register("products", ProductViewSet)
urlpatterns += router.urls
