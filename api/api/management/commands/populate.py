from django.core.management.base import BaseCommand

from nav.populate import populate as populate_nav


class Command(BaseCommand):
    help = "Pré-remplit la base de données si elle est vide"

    def handle(self, *args, **kwargs):
        populate_nav(verbose=True)
