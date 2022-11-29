from celery import shared_task
from django.core.management import call_command
from io import StringIO
from constance import config
from django.core.mail import send_mail

from urllib3.exceptions import InsecureRequestWarning
import requests
import urllib

from airfields.tasks import pull_airfields, pull_airfields_maps, get_airfieldmap_model
from radionav.tasks import pull_radionav
from acc.tasks import pull_sectors

# disable warning message when using verify=False
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


@shared_task
def download_last_airac():
    out = StringIO()
    call_command("download_last_airac", stdout=out)
    return out.getvalue().split("\n")


@shared_task
def pull_from_diapason():
    if not config.FALLBACK_URL:
        raise ValueError("FALLBACK_URL n'a pas été configuré correctement")
    session = requests.session()
    session.proxies = urllib.request.getproxies()
    pull_airfields(session)
    pull_airfields_maps(session)
    pull_radionav(session)
    pull_sectors(session)
    notify_managers()
    return True


def notify_managers():
    if config.AIRAC_UPDATE_MANAGERS:
        map_count = get_airfieldmap_model().objects.filter(pdf__isnull=False).count()
        success_message = "Les données disponibles sur Coconuts ont bien été mises à jour à partir de {} :\n{} cartes ont été téléchargées.".format(
            config.FALLBACK_URL, map_count)
        print(success_message)
        send_mail(
            '{}{}'.format(config.EMAIL_SUBJECT_PREFIX,
                          "Coconuts mis à jour grâce à {}".format(config.FALLBACK_URL)),
            success_message, config.EMAIL_ADMIN,
            config.AIRAC_UPDATE_MANAGERS.split(';'), fail_silently=False)
