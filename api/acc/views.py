from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter

from .serializers import AntennaSerializer, ControlCenterSerializer, SectorSerializer, SimpleSectorSerializer
from .models import Sector, Antenna, ControlCenter


class AntennaViewSet(ReadOnlyModelViewSet):
    '''
    Antennes pouvant être associées à un secteur
    Renseignées manuellement par l'administrateur
    '''
    serializer_class = AntennaSerializer
    queryset = Antenna.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['name']


class SectorViewSet(ReadOnlyModelViewSet):
    '''
    Secteurs de contrôle en route
    Fréquences issues de l'AIP GEN3.4
    Limites secteurs issues de l'AIP ENR2.2
    Antennes renseignées manuellement par l'administrateur
    '''
    serializer_class = SimpleSectorSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'frequencies__frequency']
    lookup_field = 'name'

    def get_serializer_class(self):
        if self.action == 'list':
            return SimpleSectorSerializer
        # use a simpler serializer for list view to improve database access efficiency ('phones' takes too long)
        return SectorSerializer

    def get_queryset(self):
        return Sector.objects\
            .select_related('control_center')\
            .prefetch_related('files', 'frequencies', 'parts',  'main_antennas', 'alternate_antennas',).all()


class ControlCenterViewSet(ReadOnlyModelViewSet):
    '''
    Centres de contrôle en route avec secteurs
    Issus de l'AIP GEN3.4
    '''
    serializer_class = ControlCenterSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        return ControlCenter.objects.prefetch_related(
            'sectors__frequencies').all()
