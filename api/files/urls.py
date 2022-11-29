from rest_framework import routers

from .views import StaticFileViewSet, FileCategoryViewSet

router = routers.SimpleRouter()
router.register(r'file', StaticFileViewSet, basename='file')
router.register(r'category', FileCategoryViewSet, basename="category")
