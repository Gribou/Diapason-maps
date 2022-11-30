from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.utils import timezone
from datetime import datetime
import traceback

from .models import CivSchedule, AzbaArea


class CivScheduleSerializer(ModelSerializer):
    sunset = SerializerMethodField()
    sunrise = SerializerMethodField()

    class Meta:
        model = CivSchedule
        fields = ['label', 'is_open', 'open_at',
                  'closed_at', 'sunset', 'sunrise']

    def get_sunset(self, obj):
        return obj.reference.ephemeris['sunset'] if obj.reference is not None else None

    def get_sunrise(self, obj):
        return obj.reference.ephemeris['sunrise'] if obj.reference is not None else None


class AzbaMapSerializer(ModelSerializer):
    class Meta:
        model = AzbaArea
        fields = ['slug', 'label', 'ceiling',
                  'floor', 'boundaries', 'pk']
