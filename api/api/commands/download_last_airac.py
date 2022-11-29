from django.core.management.base import BaseCommand
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from django.core.mail import send_mail
from constance import config

from api.utils import get_current_airac_cycle_date
from api.tasks import pull_from_diapason
from airfields.models import AirfieldFrequency, AirfieldMap
from airfields.scraper.fr_spiders.vfr_frequencies_spider import VFRFrequenciesSpider
from airfields.scraper.fr_spiders.ifr_maps_spider import IFRMapsSpider
from airfields.scraper.fr_spiders.vfr_maps_spider import VFRMapsSpider
from airfields.scraper.fr_spiders.ifr_frequencies_spider import IFRFrequenciesSpider
from airfields.scraper.fr_spiders.airfields_spider import AirfieldsSpider
from airfields.scraper.other_spiders.belgo_airfields_spider import BelgoAirfieldsSpider
from airfields.scraper.other_spiders.nats_airfields_spider import NATSAirfieldsSpider
from acc.models import SectorFrequency
from acc.scraper.spiders.sector_frequencies_spider import SectorFrequencySpider
from acc.scraper.spiders.sector_boundaries_spider import SectorBoundariesSpider, post_process as boundaries_post_process
from acc.models import SectorFrequency, SectorPart
from civ.models import AzbaArea
from civ.scraper.spiders.azba_boundaries_spider import AzbaBoundariesSpider
from radionav.scraper.spiders.fr_radionav_spider import RadionavSpider
from radionav.scraper.spiders.nats_radionav_spider import NatsRadionavSpider
from radionav.scraper.spiders.belgo_radionav_spider import BelgoRadionavSpider
from radionav.models import RadioNavStation

# update is successful is more than <> maps where downloaded
MAP_CHECK_THRESHOLD = 500


class Command(BaseCommand):
    help = "Télécharge les données du dernier cycle AIRAC depuis l'eAIP (sia.aviation-civile.gouv.fr)"

    def add_arguments(self, parser):
        parser.add_argument(
            '-f', '--force',
            action='store_true',
            help='Télécharge les données même s\'il y en a déjà pour ce cycle AIRAC en base de données',
        )

    def handle(self, *args, **kwargs):
        force = kwargs['force']
        current_airac = get_current_airac_cycle_date()
        if not force and AirfieldMap.objects.filter(airac=current_airac).exists():
            self.stdout.write(self.style.ERROR(
                "Les données pour ce cycle AIRAC existent déjà. Veuillez les supprimer avant d'en télécharger de nouvelles (python manage.py delete_airac <yyyy-mm-dd>)."))
        else:
            if force:
                self._force_clean()
            self._scrape(current_airac)
            self._clean(current_airac)
            self._check_and_notify(current_airac)
            self.stdout.write(self.style.SUCCESS("-- DONE --"))

    def _scrape(self, current_airac):
        self.stdout.write(
            "Téléchargement des données à jour depuis sia.aviation-civile.gouv.fr...")
        airac_arg = current_airac.strftime("%Y-%m-%d")
        process = CrawlerRunner(get_project_settings())
        process.crawl(AirfieldsSpider, airac=airac_arg)
        process.crawl(VFRMapsSpider, airac=airac_arg)
        process.crawl(IFRMapsSpider, airac=airac_arg)
        process.crawl(VFRFrequenciesSpider, airac=airac_arg)
        process.crawl(IFRFrequenciesSpider, airac=airac_arg)
        process.crawl(SectorFrequencySpider, airac=airac_arg)
        process.crawl(SectorBoundariesSpider, airac=airac_arg)
        process.crawl(RadionavSpider, airac=airac_arg)
        process.crawl(BelgoAirfieldsSpider, airac=airac_arg)
        process.crawl(BelgoRadionavSpider, airac=airac_arg)
        process.crawl(NATSAirfieldsSpider, airac=airac_arg)
        process.crawl(NatsRadionavSpider, airac=airac_arg)
        process.crawl(AzbaBoundariesSpider, airac=airac_arg)
        deferred = process.join()
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()

    def _force_clean(self):
        SectorPart.objects.all().delete()
        SectorFrequency.objects.all().delete()

    def _clean(self, current_airac):
        # delete items from older airac
        AirfieldMap.objects.exclude(airac=current_airac).all().delete()
        AirfieldFrequency.objects.exclude(airac=current_airac).all().delete()
        RadioNavStation.objects.exclude(airac=current_airac).all().delete()
        SectorFrequency.objects.exclude(airac=current_airac).all().delete()
        SectorPart.objects.exclude(airac=current_airac).all().delete()
        AzbaArea.objects.exclude(airac=current_airac).all().delete()
        boundaries_post_process()

    def _check_and_notify(self, airac):
        map_count = AirfieldMap.objects.filter(
            airac=airac, pdf__isnull=False).count()
        ad_freq_count = AirfieldFrequency.objects.filter(airac=airac).count()
        sector_count = SectorFrequency.objects.filter(airac=airac).count()
        radionav_count = RadioNavStation.objects.filter(airac=airac).count()
        if map_count > MAP_CHECK_THRESHOLD:
            success_message = "Les données disponibles sur Coconuts ont bien été mises à jour pour le cycle AIRAC {} :\n{} cartes ont été téléchargées.\n{} fréquences d'aérodrome mises à jour.\n{} fréquences de secteur mis à jour.\n{} moyens de radionavigation mis à jour".format(
                airac.strftime("%d/%m/%Y"), map_count, ad_freq_count, sector_count, radionav_count)
            self.stdout.write(self.style.SUCCESS(success_message))
            self._send_mail_to_managers(
                'Cartes mises à jour avec succès', success_message)
            return True
        else:
            error_message = "Aucune nouvelle carte n'a été téléchargée lors de la mise à jour de Coconuts pour le nouveau cycle AIRAC.\nLe format de sia.aviation-civile.gouv.fr a peut-être changé ?"
            if config.FALLBACK_URL:
                error_message += "\nUne tentative de récupération des données depuis l'url fallback sera déclenchée dans 30 min"
            self.stdout.write(self.style.NOTICE(error_message))
            self._send_mail_to_managers(
                'ECHEC de la mise à jour', error_message)
            # try to get data from fallback url in 30 minutes
            if config.FALLBACK_URL:
                pull_from_diapason.apply_async(countdown=60*30)
            return False

    def _send_mail_to_managers(self, subject, message):
        send_mail('{}{}'.format(config.EMAIL_SUBJECT_PREFIX, subject),
                  message, config.EMAIL_ADMIN,
                  config.AIRAC_UPDATE_MANAGERS.split(';'), fail_silently=False)
