from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r'antenna', views.AntennaViewSet, basename='antenna')
router.register(r'sector', views.SectorViewSet, basename='sector')
router.register(r'control_center', views.ControlCenterViewSet,
                basename='control_center')
