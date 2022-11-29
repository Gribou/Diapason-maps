from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from .serializers import KMLMapSerializer, LayerFolderSerializer, MapLayerSerializer
from .models import KMLMap, MapLayer, LayerFolder


class MapLayerViewSet(ModelViewSet):
    '''
        Calques pour affichage dans un module Leaflet
        Générée à partir d'un fichier MBTiles (grâce à QGIS par ex)

        Mise à jour par API possible avec un compte utilisateur adapté (POST/PUT/DELETE FormData)
    '''
    serializer_class = MapLayerSerializer
    queryset = MapLayer.objects.filter(metadata__isnull=False).all()
    lookup_field = 'slug'
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    parser_classes = [MultiPartParser]


class LayerFolderViewSet(ReadOnlyModelViewSet):
    serializer_class = LayerFolderSerializer

    def get_queryset(self):
        return [f for f in LayerFolder.objects.prefetch_related('tn_children', 'layers').all() if f.is_root()]


class KMLMapViewSet(ReadOnlyModelViewSet):
    serializer_class = KMLMapSerializer
    queryset = KMLMap.objects.all()
