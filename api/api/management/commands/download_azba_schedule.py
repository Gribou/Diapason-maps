from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from django.utils import timezone
from datetime import timedelta


from civ.models import AzbaSchedule, AzbaKnownSchedule
from civ.scraper.spiders.azba_schedule_spider import AzbaScheduleSpider


class Command(BaseCommand):
    help = "Télécharge le programme des activités AZBA"

    def handle(self, *args, **kwargs):
        self._delete_obsolete()
        self._download_new()

    def _delete_obsolete(self):
        self.stdout.write("Suppression des cartes AZBA périmées...")
        obsolete_ranges = AzbaKnownSchedule.objects.filter(
            up_to__lte=timezone.now() - timedelta(days=30))
        end = max(obsolete_ranges.values_list(
            "up_to", flat=True).all(), default=None)
        obsolete_ranges.all().delete()
        if end:
            AzbaSchedule.objects.objects.filter(
                deactivation_time__lte=end).all().delete()

    def _download_new(self):
        process = CrawlerProcess(get_project_settings())
        process.crawl(AzbaScheduleSpider)
        process.start()
