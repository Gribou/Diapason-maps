from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination


from api.utils import get_most_recent_airac_in_db
from .serializers import AirfieldMapSerializer, AirfieldSerializer, SimpleAirfieldSerializer
from .models import AirfieldMap, Airfield


class AirfieldViewSet(ReadOnlyModelViewSet):
    serializer_class = SimpleAirfieldSerializer
    queryset = Airfield.objects.prefetch_related(
        'maps', 'frequencies', 'files')
    filter_backends = [SearchFilter]
    search_fields = ['icao_code', 'name']
    lookup_field = 'icao_code'

    def get_serializer_class(self):
        if self.action == 'list':
            return SimpleAirfieldSerializer
        # use a simpler serializer for list view to improve database access efficiency ('phones' takes too long)
        return AirfieldSerializer


class AirfieldMapViewSet(ReadOnlyModelViewSet):
    '''
    Cartes d'aérodrome
    Issues de l'AIP AD2 et cartes VAC et VACH
    Vue paginée (30 résultats par page)
    '''
    serializer_class = AirfieldMapSerializer
    filter_backends = [SearchFilter]
    search_fields = ['airac', 'name', 'airfield__name', 'airfield__icao_code']
    pagination_class = PageNumberPagination

    def get_queryset(self):
        most_recent_airac_in_db = get_most_recent_airac_in_db()
        return AirfieldMap.objects.prefetch_related('airfield').filter(airac=most_recent_airac_in_db).all()


# class AirfieldFrequencyViewSet(ReadOnlyModelViewSet):
#     serializer_class = AirfieldFrequencySerializer
#     filter_backends = [SearchFilter]
#     search_fields = ['airfield__icao', 'frequency_type']

#     def get_queryset(self):
#         most_recent_airac_in_db = get_most_recent_airac_in_db()
#         return AirfieldFrequency.objects.prefetch_related('airfield').filter(airac=most_recent_airac_in_db).all()
