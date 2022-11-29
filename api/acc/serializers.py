from rest_framework.serializers import (
    ModelSerializer,
    StringRelatedField,
    SerializerMethodField,
    CharField)
from django.db.models import Q
from functools import reduce
from django.urls import reverse

from api.utils import pretty_longitude, pretty_latitude
from phones.models import Telephone
from phones.serializers import TelephoneSerializer
from files.serializers import StaticFileSerializer
from .models import Antenna, ControlCenter, Sector, SectorFrequency, SectorPart


class AntennaSerializer(ModelSerializer):
    latitude = SerializerMethodField()
    longitude = SerializerMethodField()

    class Meta:
        model = Antenna
        fields = ['pk', 'name', 'latitude', 'longitude']

    def get_latitude(self, obj):
        return pretty_latitude(obj.latitude)

    def get_longitude(self, obj):
        return pretty_longitude(obj.longitude)


class SectorFrequencySerializer(ModelSerializer):
    frequency_type = CharField(source='get_frequency_type_display')

    class Meta:
        model = SectorFrequency
        fields = ['frequency', 'frequency_type']


class SectorPartSerializer(ModelSerializer):

    class Meta:
        model = SectorPart
        fields = ['ceiling', 'floor', 'boundaries', 'pk']


class SimpleSectorSerializer(ModelSerializer):
    frequencies = SectorFrequencySerializer(many=True)
    control_center = StringRelatedField()
    global_search = SerializerMethodField()
    has_boundaries = SerializerMethodField()
    parts = SectorPartSerializer(many=True)

    class Meta:
        model = Sector
        fields = ['pk', 'control_center', 'frequencies',
                  'name', 'hidden', 'has_boundaries', 'parts', 'global_search']

    def get_global_search(self, obj):
        # pre-formatted attr to be used by global search feature (diapason-portal)
        index_url = self.context['request'].build_absolute_uri(reverse("home"))
        return {
            "title": obj.name,
            "subtitle": obj.control_center.name,
            "url": "{}sector/{}".format(index_url, obj.name)
        }

    def get_has_boundaries(self, obj):
        return obj.parts.exists()


class SectorSerializer(SimpleSectorSerializer):
    main_antennas = AntennaSerializer(many=True)
    alternate_antennas = AntennaSerializer(many=True)
    phones = SerializerMethodField()
    files = StaticFileSerializer(many=True)
    max_bounds = SerializerMethodField()

    class Meta:
        model = Sector
        fields = ['name', 'control_center', 'frequencies', 'phones',
                  'main_antennas', 'alternate_antennas', 'hidden', 'files', 'parts', 'max_bounds', 'pk']

    def get_phones(self, obj):
        # Sector phone numbers are usually prefixed with the end of ACC icao code
        ACC_SHORTCUT = ['BB', 'RR', 'EE', 'MM', 'FF']
        return TelephoneSerializer(Telephone.objects.filter(
            reduce(lambda q, value: q | Q(name__endswith=value+" "+obj.name), ACC_SHORTCUT, Q()) | Q(name__exact=obj.name)).distinct().all(), many=True, context=self.context).data

    def get_max_bounds(self, obj):
        max_lat = None
        min_lat = None
        max_lon = None
        min_lon = None
        for p in obj.parts.all():
            for lat, lon in p.boundaries:
                if max_lat is None or lat > max_lat:
                    max_lat = lat
                if min_lat is None or lat < min_lat:
                    min_lat = lat
                if max_lon is None or lon > max_lon:
                    max_lon = lon
                if min_lon is None or lon < min_lon:
                    min_lon = lon
        # top left and bottom right corner
        return [
            [max_lat, min_lon],
            [min_lat, max_lon]
        ] if max_lat is not None else None


class ControlCenterSerializer(ModelSerializer):
    sectors = SimpleSectorSerializer(many=True)

    class Meta:
        model = ControlCenter
        fields = ['name', 'rank', 'sectors', 'pk']
