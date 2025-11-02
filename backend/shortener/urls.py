from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import URLViewSet, RedirectView, HealthCheckView

router = DefaultRouter()
router.register(r'urls', URLViewSet, basename='url')

urlpatterns = [
    path('', include(router.urls)),
    path('health/', HealthCheckView.as_view(), name='health-check'),
]
