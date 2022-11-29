from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r'phone', views.TelephoneViewSet, basename='telephone')
router.register(r'category', views.TelephoneCategoryViewSet,
                basename='telephone_category')
