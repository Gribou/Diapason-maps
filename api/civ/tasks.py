from celery import shared_task
from django.core.management import call_command
from io import StringIO


@shared_task
def download_azba_schedule():
    out = StringIO()
    call_command("download_azba_schedule", stdout=out)
    return out.getvalue().split("\n")
