from rest_framework.serializers import ModelSerializer, StringRelatedField, SerializerMethodField
from django.urls import reverse

from .models import RadioNavStation
from api.utils import pretty_latitude, pretty_longitude


class RadioNavStationSerializer(ModelSerializer):
    types = StringRelatedField(many=True)
    latitude = SerializerMethodField()
    longitude = SerializerMethodField()
    global_search = SerializerMethodField()

    def get_latitude(self, obj):
        return pretty_latitude(obj.latitude)

    def get_longitude(self, obj):
        return pretty_longitude(obj.longitude)

    def get_global_search(self, obj):
        # pre-formatted attr to be used by global search feature (diapason-portal)
        index_url = self.context['request'].build_absolute_uri(reverse("home"))
        return {
            "title": obj.long_name,
            "subtitle": "{} ({})".format(obj.short_name, " ".join([t.label for t in obj.types.all()])),
            "url": "{}radionav/{}".format(index_url, obj.short_name)
        }

    class Meta:
        model = RadioNavStation
        fields = ['pk', 'short_name', 'long_name',
                  'types', 'latitude', 'longitude', 'frequency', 'range', 'global_search']
