from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r'map', views.AirfieldMapViewSet, basename='map')
router.register(r'airfield', views.AirfieldViewSet, basename='airfield')
# router.register(r'frequency', views.AirfieldFrequencyViewSet,
#                 basename='frequency')
