from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter

from .serializers import RadioNavStationSerializer
from .models import RadioNavStation


class RadioNavStationViewSet(ReadOnlyModelViewSet):
    serializer_class = RadioNavStationSerializer
    queryset = RadioNavStation.objects
    filter_backends = [SearchFilter]
    search_fields = ['short_name', 'long_name', 'types__label']
    lookup_field = 'short_name'
