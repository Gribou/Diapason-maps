from rest_framework import routers

from .views import KMLMapViewSet, LayerFolderViewSet, MapLayerViewSet

router = routers.SimpleRouter()
router.register(r'layer', MapLayerViewSet, basename="layer")
router.register(r'folder', LayerFolderViewSet, basename="layer-folder")
router.register(r'kml', KMLMapViewSet, basename="kml-map")
