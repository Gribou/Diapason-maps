from rest_framework.serializers import (
    ModelSerializer, StringRelatedField, SerializerMethodField, CharField)
from django.db.models import Q
from django.urls import reverse

from .models import AirfieldFrequency, AirfieldMap, Airfield
from api.utils import pretty_latitude, pretty_longitude
from files.serializers import StaticFileSerializer
from phones.models import Telephone
from phones.serializers import TelephoneSerializer


class AirfieldMapSerializer(ModelSerializer):
    airfield = StringRelatedField()
    global_search = SerializerMethodField()

    class Meta:
        model = AirfieldMap
        fields = ['pk', 'airfield', 'airac', 'name', 'pdf', 'global_search']

    def get_global_search(self, obj):
        # pre-formatted attr to be used by global search feature (diapason-portal)
        return {
            "title": obj.name,
            "subtitle": str(obj.airfield),
            "url": self.context['request'].build_absolute_uri(obj.pdf.url)
        }


class AirfieldFrequencySerializer(ModelSerializer):
    airfield = StringRelatedField()
    frequency_type = CharField(source="get_frequency_type_display")

    class Meta:
        model = AirfieldFrequency
        fields = ['airfield', 'value', 'frequency_type', 'comments']


class SimpleAirfieldSerializer(ModelSerializer):
    latitude = SerializerMethodField()
    longitude = SerializerMethodField()
    frequencies = AirfieldFrequencySerializer(many=True)
    global_search = SerializerMethodField()

    def get_latitude(self, obj):
        return pretty_latitude(obj.latitude)

    def get_longitude(self, obj):
        return pretty_longitude(obj.longitude)

    def get_global_search(self, obj):
        # pre-formatted attr to be used by global search feature (diapason-portal)
        index_url = self.context['request'].build_absolute_uri(reverse("home"))
        return {
            "title": obj.icao_code,
            "subtitle": obj.name,
            "url": "{}airfield/{}".format(index_url, obj.icao_code)
        }

    class Meta:
        model = Airfield
        fields = ['pk', 'icao_code', 'name', 'category',
                  'latitude', 'longitude', 'frequencies', 'ephemeris', 'global_search']


class AirfieldSerializer(SimpleAirfieldSerializer):
    maps = AirfieldMapSerializer(many=True)
    phones = SerializerMethodField()
    files = StaticFileSerializer(many=True)

    class Meta:
        model = Airfield
        fields = ['pk', 'icao_code', 'name', 'latitude', 'category', 'phones',
                  'longitude', 'elevation', 'maps', 'ephemeris', 'frequencies', 'files']

    def get_phones(self, obj):
        return TelephoneSerializer(Telephone.objects.filter(Q(name__icontains=obj.icao_code) | Q(alias__icontains=obj.icao_code)).distinct().all(), many=True, context=self.context).data
