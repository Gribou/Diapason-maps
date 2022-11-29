from django.core.management.base import BaseCommand, CommandError
from datetime import datetime

from airfields.models import AirfieldFrequency, AirfieldMap
from acc.models import SectorFrequency

# python manage.py delete_airac 2021-04-22


class Command(BaseCommand):
    help = "Supprime les cartes existantes de la base de donnée"

    def add_arguments(self, parser):
        parser.add_argument('airac_date', type=str,
                            help="Cycle AIRAC à supprimer")

    def handle(self, *args, **kwargs):
        airac_date = kwargs['airac_date']
        if airac_date:
            airac_date = datetime.strptime(
                airac_date, '%Y-%m-%d').date()
            AirfieldMap.objects.filter(airac=airac_date).all().delete()
            AirfieldFrequency.objects.filter(airac=airac_date).all().delete()
            SectorFrequency.objects.filter(airac=airac_date).all().delete()
        else:
            raise CommandError('Indiquez la date du cycle_airac à supprimer')
