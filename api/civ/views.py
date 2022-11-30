from rest_framework.viewsets import ReadOnlyModelViewSet
from django.utils import timezone
from datetime import datetime

from .serializers import CivScheduleSerializer, AzbaMapSerializer
from .models import CivSchedule, AzbaArea


class CIVScheduleViewSet(ReadOnlyModelViewSet):
    '''
    Horaires de CIV
    CIV enregistrés par l'administrateur
    Les horaires sont en fonction de l'éphéméride de la journée en cours
    '''
    serializer_class = CivScheduleSerializer
    queryset = CivSchedule.objects.all()


class AzbaMapViewSet(ReadOnlyModelViewSet):
    serializer_class = AzbaMapSerializer
    queryset = AzbaArea.objects.prefetch_related('schedules').filter(
        schedules__isnull=False)

    def get_queryset(self):
        # only return currently active areas
        try:
            reference_date = datetime.strptime(
                self.request.query_params.get('reference_date'), '%Y%m%d%H%M').replace(tzinfo=timezone.utc)
        except:
            reference_date = timezone.now()
        return super().get_queryset().filter(
            schedules__activation_time__lte=reference_date, schedules__deactivation_time__gt=reference_date).distinct().all()
