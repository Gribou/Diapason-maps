from rest_framework import routers

from .views import CIVScheduleViewSet, AzbaMapViewSet

router = routers.SimpleRouter()
router.register(r'schedule', CIVScheduleViewSet, basename="schedule")
router.register(r'azba', AzbaMapViewSet, basename="azba")
