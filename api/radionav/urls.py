from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r'station', views.RadioNavStationViewSet, basename='station')
