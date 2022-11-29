from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from constance import config
from django.conf import settings

from airfields.models import AirfieldMap, Airfield
from acc.models import Sector
from radionav.models import RadioNavStation
from civ.models import AzbaKnownSchedule
from .utils import get_most_recent_airac_in_db, get_current_airac_cycle_date


class InfoView(APIView):

    def get(self, request, format=None):
        current_airac = get_current_airac_cycle_date()
        most_recent_airac_in_db = get_most_recent_airac_in_db()
        map_count = AirfieldMap.objects.filter(
            airac=most_recent_airac_in_db).count()
        airfield_count = Airfield.objects.count()
        sector_count = Sector.objects.filter(hidden=False).count()
        radionav_count = RadioNavStation.objects.count()
        up_to_date = most_recent_airac_in_db == current_airac
        return Response({
            'displayed_airac': most_recent_airac_in_db.strftime('%Y-%m-%d') if most_recent_airac_in_db else None,
            'current_airac': current_airac,
            'azba_schedule': {
                'up_to': max(AzbaKnownSchedule.objects.values_list('up_to', flat=True).all(), default=None),
                'from': min(AzbaKnownSchedule.objects.values_list('from_d', flat=True).all(), default=None)
            },
            'up_to_date': up_to_date,
            'map_count': map_count,
            'sector_count': sector_count,
            'airfield_count': airfield_count,
            'station_count': radionav_count,
            'email_admin': config.EMAIL_ADMIN,
            'radio_coverage_enabled': config.RADIO_COVERAGE_ENABLED,
            'phones_enabled': config.PHONES_ENABLED,
            'files_enabled': config.FILES_ENABLED,
            'version': settings.VERSION_TAG
        })


class HealthCheckView(APIView):
    '''
    Vérification que le serveur web est en route
    A utiliser avec Docker-compose pour établir l'état de santé du container
    (healthcheck)
    '''

    def get(self, request, format=None):
        return Response(status=status.HTTP_204_NO_CONTENT)
