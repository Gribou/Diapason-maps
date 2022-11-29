from rest_framework import routers

from .views import HomePageItemViewSet, ToolbarItemViewSet

router = routers.SimpleRouter()
router.register(r'homepage', HomePageItemViewSet, basename='homepage')
router.register(r'toolbar', ToolbarItemViewSet, basename='toolbar')
